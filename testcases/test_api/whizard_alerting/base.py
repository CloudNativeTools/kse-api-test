# -*- coding:utf-8 -*-
"""
whizard-alerting 单接口测试基类
提供 get_for_test 函数和公共工具
"""
import json
import time
from typing import Optional, Callable, List, Tuple
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed

from apis.whizard_alerting.alerting_management.apis import (
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
from aomaker.storage import cache
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

# ==================== Session 级别预热缓存 ====================
# key: "prewarm:{type}:{cluster}:{namespace}:{name}", value: True
# 防止重复创建
_PREWARM_CACHE = set()

# 预热规则组列表，供 before_all / after_all 使用
PREWARM_GLOBAL_GROUPS = ["global-alert-standard", "global-alert-multi"]
PREWARM_HOST_CLUSTER_GROUP = "cluster-alert-standard"
PREWARM_HOST_NS_GROUP = "ns-alert-standard"
PREWARM_MEMBER_CLUSTER_GROUP = "member-cluster-alert-standard"
PREWARM_MEMBER_NS_GROUP = "member-ns-alert-standard"


def prewarm_all_rule_groups(host_cluster, test_namespace, member_cluster=None, test_namespace_member=None):
    """
    在 before_all 中调用，并发创建所有标准规则组并等待告警触发。
    session 级别只执行一次，后续调用直接返回。
    """
    tasks = []

    for group_name in PREWARM_GLOBAL_GROUPS:
        tasks.append(("global", None, None, group_name))

    tasks.append(("cluster", host_cluster, None, PREWARM_HOST_CLUSTER_GROUP))
    tasks.append(("namespace", host_cluster, test_namespace, PREWARM_HOST_NS_GROUP))

    if member_cluster:
        tasks.append(("cluster", member_cluster, None, PREWARM_MEMBER_CLUSTER_GROUP))
        tasks.append(("namespace", member_cluster, test_namespace_member, PREWARM_MEMBER_NS_GROUP))

    results = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(_do_prewarm_one, *t): t for t in tasks}
        for future in as_completed(futures):
            task = futures[future]
            rule_type, cluster, namespace, group_name = task
            success, found_alert = future.result()
            results[f"{rule_type}:{cluster}:{namespace}:{group_name}"] = (success, found_alert)

            status = "✓" if success else "✗"
            alert_status = "告警已触发" if found_alert else "告警未触发"
            logger.info(f"  {status} 预热完成: {rule_type}/{group_name} ({alert_status})")

    return results


def cleanup_all_prewarmed_rule_groups(host_cluster, test_namespace, member_cluster=None, test_namespace_member=None):
    """
    在 after_all 中调用，并发清理所有预热规则组。
    """
    tasks = []

    for group_name in PREWARM_GLOBAL_GROUPS:
        tasks.append(("global", None, None, group_name))

    tasks.append(("cluster", host_cluster, None, PREWARM_HOST_CLUSTER_GROUP))
    tasks.append(("namespace", host_cluster, test_namespace, PREWARM_HOST_NS_GROUP))

    if member_cluster:
        tasks.append(("cluster", member_cluster, None, PREWARM_MEMBER_CLUSTER_GROUP))
        tasks.append(("namespace", member_cluster, test_namespace_member, PREWARM_MEMBER_NS_GROUP))

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(_do_cleanup_one, *t): t for t in tasks}
        for future in as_completed(futures):
            task = futures[future]
            rule_type, cluster, namespace, group_name = task
            try:
                future.result()
                logger.info(f"  ✓ 清理完成: {rule_type}/{group_name}")
            except Exception as e:
                logger.warning(f"  ⚠ 清理失败: {rule_type}/{group_name} - {e}")


def _do_prewarm_one(rule_type, cluster, namespace, group_name):
    """执行单个规则组的预热：创建 + 等待告警"""
    cache_key = f"prewarm:{rule_type}:{cluster}:{namespace}:{group_name}"

    if cache_key in _PREWARM_CACHE:
        full_cache_key = f"alert_ready:{cache_key}"
        sql = f"SELECT value FROM {cache.table} WHERE var_name = ? LIMIT 1"
        result = cache.query(sql, (full_cache_key,))
        cached = json.loads(result[0]["value"]) if result else False
        return True, cached

    _PREWARM_CACHE.add(cache_key)

    if rule_type == "global":
        success = _ensure_global_rule_group(group_name)
    elif rule_type == "cluster":
        success = _ensure_cluster_rule_group(cluster, group_name)
    else:
        success = _ensure_namespace_rule_group(cluster, namespace, group_name)

    if not success:
        return False, False

    found_alert = _wait_alert_triggered(rule_type, cluster, namespace, group_name)
    cache.set(f"alert_ready:{cache_key}", found_alert)

    return True, found_alert


def _do_cleanup_one(rule_type, cluster, namespace, group_name):
    """执行单个规则组的清理（使用直接HTTP请求，避免线程安全问题）"""
    try:
        import requests
        from aomaker.storage import cache, config

        session = requests.Session()
        headers = cache.get("headers") or {}
        base_url = config.get("base_url") or ""

        if rule_type == "global":
            url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/globalrulegroups/{group_name}"
        elif rule_type == "cluster":
            url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups/{group_name}"
        else:
            url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups/{group_name}"

        resp = session.delete(url, headers=headers, timeout=30)
        status = resp.status_code
        if status in (200, 204) or status == 404:
            return
        logger.warning(f"_do_cleanup_one failed: {rule_type}/{group_name}, status={status}")
    except Exception as e:
        logger.warning(f"_do_cleanup_one failed: {rule_type}/{group_name} - {e}")


def _ensure_global_rule_group(group_name):
    """确保全局规则组存在（不存在则创建）"""
    try:
        list_api = HandleListGlobalRuleGroupsAPI(enable_schema_validation=False, response=None)
        list_api.query_params.limit = 50
        list_api.query_params.builtin = "false"
        res = list_api.send()
        if res.cached_response.raw_response.status_code != 200:
            return False
        data = res.cached_response.raw_response.json()
        for item in (data.get("items") or []):
            if item.get("metadata", {}).get("name") == group_name:
                return True

        request_body = load_test_data(
            "whizard_alerting", "alerting_management/global_rule_groups", "global_rule_group_custom"
        )
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"
        request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{group_name}-summary"

        create_api = HandleCreateGlobalRuleGroupAPI(request_body=request_body, enable_schema_validation=False)
        create_res = create_api.send()
        return create_res.cached_response.raw_response.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"_ensure_global_rule_group failed: {e}")
        return False


def _ensure_cluster_rule_group(cluster, group_name):
    """确保集群规则组存在（使用直接HTTP请求，避免线程安全问题）"""
    import traceback
    try:
        import requests
        from aomaker.storage import cache, config

        session = requests.Session()
        headers = cache.get("headers") or {}
        base_url = config.get("base_url") or ""

        list_url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups?limit=50&page=&ascending="
        resp = session.get(list_url, headers=headers, timeout=30)
        if resp.status_code != 200:
            logger.warning(f"_ensure_cluster_rule_group list failed: {resp.status_code}")
            return False

        data = resp.json()
        for item in (data.get("items") or []):
            if item.get("metadata", {}).get("name") == group_name:
                return True

        request_body = load_test_data(
            "whizard_alerting", "alerting_management/cluster_rule_groups", "cluster_rule_group_custom"
        )
        if not isinstance(request_body, dict):
            logger.warning(f"_ensure_cluster_rule_group: request_body is not dict, type={type(request_body)}, value={str(request_body)[:200]}")
            return False
        request_body["metadata"]["name"] = group_name

        create_url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups"
        create_resp = session.post(create_url, json=request_body, headers=headers, timeout=30)
        if create_resp.status_code not in (200, 201):
            logger.warning(f"_ensure_cluster_rule_group create failed: {create_resp.status_code} - {create_resp.text[:500]}")
        return create_resp.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"_ensure_cluster_rule_group failed: {e}\n{traceback.format_exc()}")
        return False


def _ensure_namespace_rule_group(cluster, namespace, group_name):
    """确保命名空间规则组存在（使用直接HTTP请求，避免线程安全问题）"""
    import traceback
    try:
        import requests
        from aomaker.storage import cache, config

        session = requests.Session()
        headers = cache.get("headers") or {}
        base_url = config.get("base_url") or ""

        list_url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups?limit=50"
        resp = session.get(list_url, headers=headers, timeout=30)
        if resp.status_code != 200:
            logger.warning(f"_ensure_namespace_rule_group list failed: {resp.status_code}")
            return False

        data = resp.json()
        for item in (data.get("items") or []):
            if item.get("metadata", {}).get("name") == group_name:
                return True

        request_body = load_test_data(
            "whizard_alerting", "alerting_management/namespace_rule_groups", "namespace_rule_group_custom"
        )
        if not isinstance(request_body, dict):
            logger.warning(f"_ensure_namespace_rule_group: request_body is not dict, type={type(request_body)}, value={str(request_body)[:200]}")
            return False
        request_body["metadata"]["name"] = group_name
        request_body["metadata"]["namespace"] = namespace
        request_body["spec"]["rules"][0]["alert"] = f"{group_name}-custom"
        request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{group_name}-summary"

        create_url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups"
        create_resp = session.post(create_url, json=request_body, headers=headers, timeout=30)
        if create_resp.status_code not in (200, 201):
            logger.warning(f"_ensure_namespace_rule_group create failed: {create_resp.status_code} - {create_resp.text[:500]}")
        return create_resp.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"_ensure_namespace_rule_group failed: {e}\n{traceback.format_exc()}")
        return False


def _wait_alert_triggered(rule_type, cluster, namespace, group_name):
    """等待告警触发（使用直接HTTP请求，避免线程安全问题）"""
    try:
        import requests
        from aomaker.storage import cache, config

        session = requests.Session()
        headers = cache.get("headers") or {}
        base_url = config.get("base_url") or ""

        params = {"page": "1", "limit": "10", "sortBy": "createTime", "builtin": "false"}
        if group_name:
            params["label_filters"] = f"rule_group={group_name}"

        if rule_type == "global":
            url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/globalalerts"
        elif rule_type == "cluster":
            url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusteralerts"
        else:
            url = f"{base_url}/proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/alerts"

        def query_func():
            try:
                resp = session.get(url, headers=headers, params=params, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("items") or []
                return None
            except Exception:
                return None

        found_alert, _ = wait_for_alerts(query_func, max_attempts=48, sleep_interval=5)
        return found_alert
    except Exception as e:
        logger.warning(f"_wait_alert_triggered failed: {e}")
        return False


def is_alert_prewarmed(rule_type, cluster=None, namespace=None, group_name=None):
    """检查告警是否已预热（已触发）"""
    cache_key = f"alert_ready:prewarm:{rule_type}:{cluster}:{namespace}:{group_name}"
    sql = f"SELECT value FROM {cache.table} WHERE var_name = ? LIMIT 1"
    result = cache.query(sql, (cache_key,))
    if result:
        return json.loads(result[0]["value"])
    return False

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
        request_body = load_test_data("whizard_alerting", "alerting_management/global_rule_groups", "global_rule_group_custom")
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
        logger.warning(f"get_for_test_global_rule_group failed: {e}")
        return False


def cleanup_global_rule_group(group_name: str) -> bool:
    """清理全局规则组测试数据"""
    try:
        api = HandleDeleteGlobalRuleGroupAPI(
            path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(name=group_name),
            enable_schema_validation=False,
            response=None
        )
        res = api.send()
        status = res.cached_response.raw_response.status_code
        return status in (200, 204) or status == 404
    except Exception as e:
        logger.warning(f"cleanup_global_rule_group failed: {e}")
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
                logger.warning(f"查询规则组列表失败: {res.cached_response.raw_response.status_code}")
                return False

            data = res.cached_response.raw_response.json()

            # 2. 检查测试数据是否已存在
            for item in (data.get("items") or []):
                if item.get("metadata", {}).get("name") == group_name:
                    logger.info(f"规则组 {group_name} 已存在")
                    return True

            # 3. 测试数据不存在，创建它（使用自定义规则组模板，expr: vector(1) 无需查询节点）
            request_body = load_test_data("whizard_alerting", "alerting_management/cluster_rule_groups", "cluster_rule_group_custom")
            request_body["metadata"]["name"] = group_name

            create_api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            create_res = create_api.send()
            logger.info(f"创建规则组 {group_name} 响应: {create_res.cached_response.raw_response.status_code}")

            if create_res.cached_response.raw_response.status_code in (200, 201):
                return True
            logger.warning(f"创建规则组失败: {create_res.cached_response.raw_response.text[:200]}")
            return False
        finally:
            clear_current_cluster()

    except Exception as e:
        logger.warning(f"get_for_test_cluster_rule_group failed: {e}")
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
                enable_schema_validation=False,
                response=None
            )
            res = api.send()
            status = res.cached_response.raw_response.status_code
            return status in (200, 204) or status == 404
        finally:
            clear_current_cluster()
    except Exception as e:
        logger.warning(f"cleanup_cluster_rule_group failed: {e}")
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
            request_body = load_test_data("whizard_alerting", "alerting_management/namespace_rule_groups", "namespace_rule_group_custom")
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
                logger.info(f"创建成功: {group_name}")
                return True
            logger.warning(f"创建失败 {group_name}，状态码: {create_res.cached_response.raw_response.status_code}, 响应: {create_res.cached_response.raw_response.text[:200]}")
            return False
        finally:
            clear_current_cluster()

    except Exception as e:
        logger.warning(f"get_for_test_namespace_rule_group failed: {e}")
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
                enable_schema_validation=False,
                response=None
            )
            res = api.send()
            status = res.cached_response.raw_response.status_code
            if status in (200, 204) or status == 404:
                logger.info(f"清理成功: {group_name}")
                return True
            logger.warning(f"清理失败 {group_name}，状态码: {status}")
            return False
        finally:
            clear_current_cluster()
    except Exception as e:
        logger.warning(f"清理异常 {group_name}: {e}")
        return False


# ==================== 告警数据动态解析 ====================

def resolve_alerting_data(data: dict, host_cluster: str = None, member_cluster: str = None) -> dict:
    """
    解析告警测试数据中的动态占位符

    支持的占位符（字符串形式）：
    - __DYNAMIC_HOST_NODES__: 替换为 Host 集群节点名称列表
    - __DYNAMIC_MEMBER_NODES__: 替换为 Member 集群节点名称列表

    Args:
        data: 从 load_test_data 加载的数据（已变量替换）
        host_cluster: Host 集群名称
        member_cluster: Member 集群名称

    Returns:
        处理后的 dict
    """
    import copy
    from utils.cluster_helpers import get_cluster_nodes

    result = copy.deepcopy(data)
    _node_cache = {}

    def _get_nodes(cluster):
        if cluster not in _node_cache:
            _node_cache[cluster] = get_cluster_nodes(cluster) if cluster else []
        return _node_cache[cluster]

    def _resolve(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if isinstance(v, str):
                    if v == "__DYNAMIC_HOST_NODES__":
                        obj[k] = _get_nodes(host_cluster)
                    elif v == "__DYNAMIC_MEMBER_NODES__":
                        obj[k] = _get_nodes(member_cluster)
                else:
                    _resolve(v)
        elif isinstance(obj, list):
            for i, item in enumerate(list(obj)):
                if isinstance(item, str):
                    if item == "__DYNAMIC_HOST_NODES__":
                        obj[i] = _get_nodes(host_cluster)
                    elif item == "__DYNAMIC_MEMBER_NODES__":
                        obj[i] = _get_nodes(member_cluster)
                else:
                    _resolve(item)

    _resolve(result)
    return result


def load_alerting_test_data(module_path: str, data_key: str) -> dict:
    """
    加载 whizard_alerting 测试数据，自动解析动态占位符

    Args:
        module_path: 模块路径，如 "alerting_management/global_rule_groups"
        data_key: 数据键名，如 "global_rule_group_template_node_single"

    Returns:
        已处理变量替换和动态占位符的数据 dict
    """
    from utils.cluster_helpers import get_clusters

    data = load_test_data("whizard_alerting", module_path, data_key, replace_vars=True)
    host_cluster, member_cluster = get_clusters()
    return resolve_alerting_data(data, host_cluster=host_cluster, member_cluster=member_cluster)


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
            logger.info(f"找到告警，状态: {[item.get('state') for item in items]}")
            break

        if attempt < max_attempts - 1:
            time.sleep(sleep_interval)

    if not found_alert:
        logger.warning("告警未触发，可能测试环境无监控数据")

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
    from apis.whizard_alerting.alerting_management.apis import HandleListClusterAlertsAPI

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
    from apis.whizard_alerting.alerting_management.apis import HandleListAlertsAPI

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
    from apis.whizard_alerting.alerting_management.apis import HandleListGlobalAlertsAPI

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
