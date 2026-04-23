# -*- coding:utf-8 -*-
"""
whizard-alerting 单接口测试基类
提供 get_for_test 函数和公共工具
"""
import time
from typing import Optional, Callable, List, Tuple

from apis.whizard_alerting.Alerting_Management.apis import (
    HandleListGlobalRuleGroupsAPI,
    HandleCreateGlobalRuleGroupAPI,
    HandleDeleteGlobalRuleGroupAPI,
    HandleListClusterRuleGroupsAPI,
    HandleCreateClusterRuleGroupAPI,
    HandleDeleteClusterRuleGroupAPI,
    HandleListRuleGroupsAPI,
    HandleCreateRuleGroupAPI,
    HandleDeleteRuleGroupAPI,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster


# ==================== Global Rule Group ====================

def get_for_test_global_rule_group(group_name: str) -> bool:
    """
    获取全局规则组测试数据
    1. 先查询，如果测试数据已存在，直接返回 True
    2. 如果测试数据不存在，调用创建 API 创建测试数据
    3. 创建成功返回 True，失败返回 False
    """
    try:
        # 1. 查询现有数据
        list_api = HandleListGlobalRuleGroupsAPI(
            enable_schema_validation=False,
            response=None
        )
        list_api.query_params.limit = 10
        list_api.query_params.builtin = "false"
        list_api.query_params.sortBy = "createTime"

        res = list_api.send()

        if res.cached_response.raw_response.status_code != 200:
            return False

        data = res.cached_response.raw_response.json()

        # 2. 检查测试数据是否已存在
        for item in (data.get("items") or []):
            if item.get("metadata", {}).get("name") == group_name:
                return True

        # 3. 测试数据不存在，创建它
        request_body = load_test_data("whizard_alerting", "Alerting_Management/global_rule_groups", "global_rule_group_custom")
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"

        create_api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        create_res = create_api.send()

        if create_res.cached_response.raw_response.status_code in (200, 201):
            return True
        return False

    except Exception as e:
        print(f"get_for_test_global_rule_group failed: {e}")
        return False


def cleanup_global_rule_group(group_name: str) -> bool:
    """清理全局规则组测试数据"""
    try:
        api = HandleDeleteGlobalRuleGroupAPI(
            path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(name=group_name),
            enable_schema_validation=False
        )
        res = api.send()
        return res.cached_response.raw_response.status_code in (200, 204)
    except Exception as e:
        print(f"cleanup_global_rule_group failed: {e}")
        return False


# ==================== Cluster Rule Group ====================

def get_for_test_cluster_rule_group(cluster: str, group_name: str) -> bool:
    """
    获取集群规则组测试数据
    """
    try:
        # 设置当前集群，让中间件自动添加 /clusters/{cluster} 前缀
        set_current_cluster(cluster)

        try:
            # 1. 查询现有数据
            list_api = HandleListClusterRuleGroupsAPI(
                path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=cluster)
            )
            # 修复查询参数默认值问题
            list_api.query_params.page = None
            list_api.query_params.ascending = None
            res = list_api.send()

            if res.cached_response.raw_response.status_code != 200:
                print(f"查询规则组列表失败: {res.cached_response.raw_response.status_code}")
                return False

            data = res.cached_response.raw_response.json()

            # 2. 检查测试数据是否已存在
            for item in (data.get("items") or []):
                if item.get("metadata", {}).get("name") == group_name:
                    print(f"规则组 {group_name} 已存在")
                    return True

            # 3. 测试数据不存在，创建它（使用自定义规则组模板，expr: vector(1) 无需查询节点）
            request_body = load_test_data("whizard_alerting", "Alerting_Management/cluster_rule_groups", "cluster_rule_group_custom")
            request_body["metadata"]["name"] = group_name

            create_api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            create_res = create_api.send()
            print(f"创建规则组 {group_name} 响应: {create_res.cached_response.raw_response.status_code}")

            if create_res.cached_response.raw_response.status_code in (200, 201):
                return True
            print(f"创建规则组失败: {create_res.cached_response.raw_response.text[:200]}")
            return False
        finally:
            clear_current_cluster()

    except Exception as e:
        print(f"get_for_test_cluster_rule_group failed: {e}")
        return False


def cleanup_cluster_rule_group(cluster: str, group_name: str) -> bool:
    """清理集群规则组测试数据"""
    try:
        set_current_cluster(cluster)
        try:
            api = HandleDeleteClusterRuleGroupAPI(
                path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                    cluster=cluster,
                    name=group_name
                ),
                enable_schema_validation=False
            )
            res = api.send()
            return res.cached_response.raw_response.status_code in (200, 204)
        finally:
            clear_current_cluster()
    except Exception as e:
        print(f"cleanup_cluster_rule_group failed: {e}")
        return False


# ==================== Namespace Rule Group ====================

def get_for_test_namespace_rule_group(cluster: str, namespace: str, group_name: str) -> bool:
    """
    获取命名空间规则组测试数据
    """
    try:
        # 设置当前集群
        set_current_cluster(cluster)

        try:
            # 1. 查询现有数据
            list_api = HandleListRuleGroupsAPI(
                path_params=HandleListRuleGroupsAPI.PathParams(cluster=cluster, namespace=namespace),
                enable_schema_validation=False,
                response=None
            )
            list_api.query_params.limit = 10
            list_api.query_params.sortBy = "createTime"
            res = list_api.send()

            if res.cached_response.raw_response.status_code != 200:
                return False

            data = res.cached_response.raw_response.json()

            # 2. 检查测试数据是否已存在
            for item in (data.get("items") or []):
                if item.get("metadata", {}).get("name") == group_name:
                    return True

            # 3. 测试数据不存在，创建它
            request_body = load_test_data("whizard_alerting", "Alerting_Management/namespace_rule_groups", "namespace_rule_group_custom")
            request_body["metadata"]["name"] = group_name
            request_body["metadata"]["namespace"] = namespace
            request_body["spec"]["rules"][0]["alert"] = f"{group_name}-custom"
            request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{group_name}-summary"

            create_api = HandleCreateRuleGroupAPI(
                path_params=HandleCreateRuleGroupAPI.PathParams(cluster=cluster, namespace=namespace),
                request_body=request_body,
                enable_schema_validation=False,
                response=None
            )
            create_res = create_api.send()

            if create_res.cached_response.raw_response.status_code in (200, 201):
                print(f"✅ 创建成功: {group_name}")
                return True
            print(f"❌ 创建失败 {group_name}，状态码: {create_res.cached_response.raw_response.status_code}, 响应: {create_res.cached_response.raw_response.text[:200]}")
            return False
        finally:
            clear_current_cluster()

    except Exception as e:
        print(f"get_for_test_namespace_rule_group failed: {e}")
        return False


def cleanup_namespace_rule_group(cluster: str, namespace: str, group_name: str) -> bool:
    """清理命名空间规则组测试数据"""
    try:
        set_current_cluster(cluster)
        try:
            api = HandleDeleteRuleGroupAPI(
                path_params=HandleDeleteRuleGroupAPI.PathParams(
                    cluster=cluster,
                    namespace=namespace,
                    name=group_name
                ),
                enable_schema_validation=False
            )
            res = api.send()
            if res.cached_response.raw_response.status_code in (200, 204):
                print(f"🧹 清理成功: {group_name}")
                return True
            print(f"⚠️ 清理失败 {group_name}，状态码: {res.cached_response.raw_response.status_code}")
            return False
        finally:
            clear_current_cluster()
    except Exception as e:
        print(f"⚠️ 清理异常 {group_name}: {e}")
        return False


# ==================== 公共工具函数 ====================

def generate_test_name(prefix: str = "test") -> str:
    """生成测试资源名称"""
    return f"{prefix}-{int(time.time())}"


def build_patch_body_for_alias_desc(current_data: dict, alias_name: str, description: str) -> dict:
    """
    构建用于编辑别名和描述的 Patch 请求体

    从 GET 返回的完整数据中移除不需要的字段，然后修改 metadata.annotations
    适用于 ClusterRuleGroup、GlobalRuleGroup、RuleGroup 等资源的 Patch 操作

    Args:
        current_data: GET 接口返回的完整数据
        alias_name: 新的别名
        description: 新的描述

    Returns:
        处理后的 Patch 请求体
    """
    return build_rule_group_body(
        current_data=current_data,
        target="metadata",
        alias_name=alias_name,
        description=description,
        remove_resource_version=True
    )


def build_update_body_for_rules_annotations(current_data: dict, summary: str, message: str) -> dict:
    """
    构建用于修改规则注解的 PUT 请求体

    从 GET 返回的完整数据中移除不需要的字段，然后修改 spec.rules[].annotations
    保留 resourceVersion 用于并发控制

    Args:
        current_data: GET 接口返回的完整数据
        summary: 新的 summary
        message: 新的 message

    Returns:
        处理后的 PUT 请求体
    """
    return build_rule_group_body(
        current_data=current_data,
        target="spec_rules",
        summary=summary,
        message=message,
        remove_resource_version=False
    )


def build_rule_group_body(
    current_data: dict,
    target: str,
    alias_name: str = None,
    description: str = None,
    summary: str = None,
    message: str = None,
    remove_resource_version: bool = True
) -> dict:
    """
    构建规则组更新请求体

    Args:
        current_data: GET 接口返回的完整数据
        target: 修改目标 - "metadata" 或 "spec_rules"
        alias_name: metadata annotations 的别名 (target="metadata" 时使用)
        description: metadata annotations 的描述 (target="metadata" 时使用)
        summary: spec rules annotations 的 summary (target="spec_rules" 时使用)
        message: spec rules annotations 的 message (target="spec_rules" 时使用)
        remove_resource_version: 是否移除 resourceVersion (PATCH 为 True, PUT 为 False)

    Returns:
        处理后的请求体
    """
    import copy

    body = copy.deepcopy(current_data)

    metadata = body.get("metadata", {})
    metadata.pop("uid", None)
    metadata.pop("generation", None)
    metadata.pop("managedFields", None)
    if remove_resource_version:
        metadata.pop("resourceVersion", None)
    body.pop("status", None)

    if target == "metadata":
        if "annotations" not in metadata:
            metadata["annotations"] = {}
        metadata["annotations"]["kubesphere.io/alias-name"] = alias_name
        metadata["annotations"]["kubesphere.io/description"] = description
    elif target == "spec_rules":
        rules = body.get("spec", {}).get("rules", [])
        if rules:
            rules[0]["annotations"] = {
                "summary": summary,
                "message": message
            }

    return body


# ==================== 告警查询公共方法 ====================

def wait_for_alerts(
    query_func: Callable[[], Optional[List[dict]]],
    max_attempts: int = 48,
    sleep_interval: int = 5,
    validate_func: Callable[[List[dict]], None] = None
) -> Tuple[bool, List[dict]]:
    """
    等待告警触发（轮询查询）

    适用于 cluster、namespace、global 各级别告警测试

    Args:
        query_func: 发送告警查询的可调用对象，返回告警 items 列表（查询失败返回 None）
        max_attempts: 最大尝试次数，默认 48 次（约 240 秒）
        sleep_interval: 每次间隔秒数，默认 5 秒
        validate_func: 对每个告警 item 做额外验证的可选函数

    Returns:
        (found_alert: bool, items: list)
    """
    found_alert = False
    items = []

    for attempt in range(max_attempts):
        items = query_func()

        if items is not None and len(items) >= 1:
            found_alert = True
            # 执行额外验证
            if validate_func:
                validate_func(items)
            print(f"找到告警，状态: {[item.get('state') for item in items]}")
            break

        if attempt < max_attempts - 1:
            time.sleep(sleep_interval)

    if not found_alert:
        print("告警未触发，可能测试环境无监控数据")

    return found_alert, items


def query_cluster_alerts(cluster: str, rule_group_name: str = None, state: str = None) -> Optional[List[dict]]:
    """
    查询集群告警列表，返回 items 列表（查询失败返回 None）

    Args:
        cluster: 集群名称
        rule_group_name: 规则组名称过滤（可选）
        state: 告警状态过滤 firing/pending（可选）

    Returns:
        告警 items 列表，或 None（查询失败）
    """
    from apis.whizard_alerting.Alerting_Management.apis import HandleListClusterAlertsAPI

    set_current_cluster(cluster)
    try:
        api = HandleListClusterAlertsAPI(
            path_params=HandleListClusterAlertsAPI.PathParams(cluster=cluster),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"
        api.query_params.builtin = "false"
        if rule_group_name:
            api.query_params.label_filters = f"rule_group={rule_group_name}"
        if state:
            api.query_params.state = state

        res = api.send()
        if res.cached_response.raw_response.status_code == 200:
            data = res.cached_response.raw_response.json()
            return data.get("items") or []
        return None
    finally:
        clear_current_cluster()

def query_namespace_alerts(cluster: str, namespace: str, rule_group_name: str = None, state: str = None) -> Optional[List[dict]]:
    """
    查询命名空间告警列表，返回 items 列表（查询失败返回 None）

    Args:
        cluster: 集群名称
        namespace: 命名空间名称
        rule_group_name: 规则组名称过滤（可选）
        state: 告警状态过滤 firing/pending（可选）

    Returns:
        告警 items 列表，或 None（查询失败）
    """
    from apis.whizard_alerting.Alerting_Management.apis import HandleListAlertsAPI

    set_current_cluster(cluster)
    try:
        api = HandleListAlertsAPI(
            path_params=HandleListAlertsAPI.PathParams(cluster=cluster, namespace=namespace),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"
        if rule_group_name:
            api.query_params.label_filters = f"rule_group={rule_group_name}"
        if state:
            api.query_params.state = state

        res = api.send()
        if res.cached_response.raw_response.status_code == 200:
            data = res.cached_response.raw_response.json()
            return data.get("items") or []
        return None
    finally:
        clear_current_cluster()


def query_global_alerts(rule_group_name: str = None, state: str = None) -> Optional[List[dict]]:
    """
    查询全局告警列表，返回 items 列表（查询失败返回 None）

    Args:
        rule_group_name: 规则组名称过滤（可选）
        state: 告警状态过滤 firing/pending（可选）

    Returns:
        告警 items 列表，或 None（查询失败）
    """
    from apis.whizard_alerting.Alerting_Management.apis import HandleListGlobalAlertsAPI

    api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
    api.query_params.page = "1"
    api.query_params.limit = "10"
    api.query_params.ascending = None
    if rule_group_name:
        api.query_params.label_filters = f"rule_group={rule_group_name}"
    if state:
        api.query_params.state = state

    res = api.send()
    if res.cached_response.raw_response.status_code == 200:
        data = res.cached_response.raw_response.json()
        return data.get("items") or []
    return None
