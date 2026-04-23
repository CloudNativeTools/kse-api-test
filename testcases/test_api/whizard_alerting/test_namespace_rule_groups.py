# -*- coding:utf-8 -*-
"""
项目规则组单接口测试
API: HandleList/Create/Get/Update/Delete/Patch RuleGroupAPI

测试策略：
1. 使用标准资源（固定名称）贯穿所有接口测试
2. get_for_test 确保资源存在（查不到就创建）
3. 创建接口单独测试（创建新资源，类级别统一清理）
4. 模块级 cleanup 兜底清理
"""
import pytest
import time
import logging

from apis.whizard_alerting.Alerting_Management.apis import (
    HandleListRuleGroupsAPI,
    HandleCreateRuleGroupAPI,
    HandleGetRuleGroupAPI,
    HandleUpdateRuleGroupAPI,
    HandleDeleteRuleGroupAPI,
    HandlePatchRuleGroupAPI,
)
from testcases.test_api.whizard_alerting.base import (
    get_for_test_namespace_rule_group,
    cleanup_namespace_rule_group,
    generate_test_name,
    build_patch_body_for_alias_desc,
    build_update_body_for_rules_annotations,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

logger = logging.getLogger(__name__)

# 标准资源名称（固定，不带时间戳）
HOST_STANDARD_RULE_GROUP = "ns-alert-standard"
MEMBER_STANDARD_RULE_GROUP = "member-ns-alert-standard"


@pytest.fixture(scope="module")
def cleanup_host_standard(host_cluster, test_namespace):
    """模块级清理：清理 host项目 标准资源"""
    yield
    try:
        cleanup_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP)
    except Exception as e:
        logger.warning(f"清理 host 项目标准规则组失败: {e}")


# ==================== Create ====================

@pytest.mark.alerting_management
class TestCreateNamespaceRuleGroup:
    """创建项目规则组 - 创建新资源（带时间戳），类级别统一清理"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_created_groups(self, host_cluster, test_namespace):
        """类级别 fixture：收集测试创建的资源名，统一清理"""
        created_groups = []
        yield created_groups

        for group_name in created_groups:
            try:
                cleanup_namespace_rule_group(host_cluster, test_namespace, group_name)
            except Exception as e:
                logger.warning(f"清理失败 {group_name}: {e}")

    def test_create_template_rule_group(self, host_cluster, test_namespace, cleanup_created_groups):
        """
        创建项目模板规则组（使用 exprBuilder - workload） //TODO: 需补充前置条件workload数据准备
        验证点：
        1. 创建成功（200/201）
        2. 返回的 metadata.name 正确
        3. 返回的 spec.rules 结构正确
        """
        group_name = generate_test_name("ns-alert")

        set_current_cluster(host_cluster)
        try:
            # 1. 从数据文件加载模板并替换占位符
            request_body = load_test_data(
                "whizard_alerting", "Alerting_Management/namespace_rule_groups", "namespace_rule_group_template"
            )
            request_body["metadata"]["name"] = group_name
            request_body["metadata"]["namespace"] = test_namespace
            request_body["spec"]["rules"][0]["alert"] = group_name
            request_body["spec"]["rules"][0]["annotations"]["summary"] = group_name

            api = HandleCreateRuleGroupAPI(
                path_params=HandleCreateRuleGroupAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            # 2. 验证响应状态码
            assert res.cached_response.raw_response.status_code in (200, 201), \
                f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

            # 3. 验证返回数据
            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == group_name
            assert "spec" in data and "rules" in data["spec"]
            assert len(data["spec"]["rules"]) > 0
            assert "exprBuilder" in data["spec"]["rules"][0]

            cleanup_created_groups.append(group_name)
            logger.info(f"模板规则组创建成功: {group_name}")
        finally:
            clear_current_cluster()

    def test_create_custom_rule_group(self, host_cluster, test_namespace, cleanup_created_groups):
        """
        创建项目自定义规则组（使用 expr: vector(1)）
        验证点：
        1. 创建成功（200/201）
        2. 返回的 metadata.name 正确
        3. 返回的 spec.rules[].expr = vector(1)
        """
        group_name = generate_test_name("ns-custom-alert")

        set_current_cluster(host_cluster)
        try:
            # 1. 从数据文件加载模板并替换占位符
            request_body = load_test_data(
                "whizard_alerting", "Alerting_Management/namespace_rule_groups", "namespace_rule_group_custom"
            )
            request_body["metadata"]["name"] = group_name
            request_body["metadata"]["namespace"] = test_namespace
            request_body["spec"]["rules"][0]["alert"] = f"{group_name}-custom"
            request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{group_name}-summary"

            api = HandleCreateRuleGroupAPI(
                path_params=HandleCreateRuleGroupAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            # 2. 验证响应状态码
            assert res.cached_response.raw_response.status_code in (200, 201), \
                f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

            # 3. 验证返回数据
            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == group_name
            assert "spec" in data and "rules" in data["spec"]
            rules = data["spec"]["rules"]
            assert len(rules) > 0
            assert rules[0].get("expr") == "vector(1)", f"自定义规则组的 expr 不正确: {rules[0].get('expr')}"

            cleanup_created_groups.append(group_name)
            logger.info(f"自定义规则组创建成功: {group_name}")
        finally:
            clear_current_cluster()


# ==================== List ====================

@pytest.mark.alerting_management
class TestListNamespaceRuleGroups:
    """查询项目规则组列表"""

    def test_list_success(self, host_cluster, test_namespace, cleanup_host_standard):
        """正常查询列表"""
        # 确保标准资源存在
        if not get_for_test_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleListRuleGroupsAPI(
                path_params=HandleListRuleGroupsAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                enable_schema_validation=False
            )
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data
            assert "totalItems" in data
        finally:
            clear_current_cluster()

    def test_list_with_name_filter(self, host_cluster, test_namespace, cleanup_host_standard):
        """按名称过滤 - 查询标准资源"""
        # 确保标准资源存在
        if not get_for_test_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleListRuleGroupsAPI(
                path_params=HandleListRuleGroupsAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                enable_schema_validation=False
            )
            api.query_params.name = HOST_STANDARD_RULE_GROUP
            api.query_params.page = 1
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            found = any(
                item.get("metadata", {}).get("name") == HOST_STANDARD_RULE_GROUP
                for item in (data.get("items") or [])
            )
            assert found, f"未找到标准规则组: {HOST_STANDARD_RULE_GROUP}"
        finally:
            clear_current_cluster()


# ==================== Get ====================

@pytest.mark.alerting_management
class TestGetNamespaceRuleGroup:
    """获取项目规则组详情"""

    def test_get_success(self, host_cluster, test_namespace, cleanup_host_standard):
        """查看规则组详情 - 使用标准资源"""
        # 确保标准资源存在
        if not get_for_test_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleGetRuleGroupAPI(
                path_params=HandleGetRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=HOST_STANDARD_RULE_GROUP
                ),
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == HOST_STANDARD_RULE_GROUP
        finally:
            clear_current_cluster()

    def test_get_not_found(self, host_cluster, test_namespace):
        """获取不存在的规则组"""
        set_current_cluster(host_cluster)
        try:
            api = HandleGetRuleGroupAPI(
                path_params=HandleGetRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name="nonexistent-group"
                ),
                enable_schema_validation=False,
                response=None
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 404
        finally:
            clear_current_cluster()


# ==================== Update ====================

@pytest.mark.alerting_management
class TestUpdateNamespaceRuleGroup:
    """更新项目规则组"""

    def test_update_success(self, host_cluster, test_namespace, cleanup_host_standard):
        """修改规则组 - 使用标准资源"""
        # 确保标准资源存在
        if not get_for_test_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            # 1. 先 GET 获取当前规则组完整数据
            get_api = HandleGetRuleGroupAPI(
                path_params=HandleGetRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=HOST_STANDARD_RULE_GROUP
                ),
                enable_schema_validation=False
            )
            get_res = get_api.send()
            current_data = get_res.cached_response.raw_response.json()

            # 2. 使用公共方法构建 PUT 请求体（修改 spec.rules[].annotations，保留 resourceVersion）
            request_body = build_update_body_for_rules_annotations(
                current_data=current_data,
                summary="updated-namespace-alert-summary",
                message="updated desc"
            )

            # 3. 发送更新请求
            api = HandleUpdateRuleGroupAPI(
                path_params=HandleUpdateRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=HOST_STANDARD_RULE_GROUP
                ),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            # 4. 验证规则注解已更新
            data = res.cached_response.raw_response.json()
            annotations = data.get("spec", {}).get("rules", [{}])[0].get("annotations", {})
            assert annotations.get("summary") == "updated-namespace-alert-summary", "summary 应已更新"
            assert annotations.get("message") == "updated desc", "message 应已更新"
        finally:
            clear_current_cluster()


# ==================== Patch ====================

@pytest.mark.alerting_management
class TestPatchNamespaceRuleGroup:
    """部分更新项目规则组（Patch）"""

    def test_patch_edit_alias_and_description(self, host_cluster, test_namespace, cleanup_host_standard):
        """
        编辑规则组别名和描述
        场景：通过 Patch 修改 metadata.annotations 中的 alias-name 和 description
        """
        # 确保标准资源存在
        if not get_for_test_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            # 1. 先 GET 获取当前规则组完整数据
            get_api = HandleGetRuleGroupAPI(
                path_params=HandleGetRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=HOST_STANDARD_RULE_GROUP
                ),
                enable_schema_validation=False
            )
            get_res = get_api.send()
            current_data = get_res.cached_response.raw_response.json()

            # 2. 使用公共方法构建 Patch 请求体
            request_body = build_patch_body_for_alias_desc(
                current_data=current_data,
                alias_name="ns-alias-updated",
                description="ns-desc-updated"
            )

            # 3. 发送 Patch 请求
            api = HandlePatchRuleGroupAPI(
                path_params=HandlePatchRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=HOST_STANDARD_RULE_GROUP
                ),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            # 4. 验证别名和描述已更新
            data = res.cached_response.raw_response.json()
            annotations = data.get("metadata", {}).get("annotations", {})
            assert annotations.get("kubesphere.io/alias-name") == "ns-alias-updated", "别名应已更新"
            assert annotations.get("kubesphere.io/description") == "ns-desc-updated", "描述应已更新"
        finally:
            clear_current_cluster()


# ==================== Delete ====================

@pytest.mark.alerting_management
class TestDeleteNamespaceRuleGroup:
    """删除项目规则组"""

    def test_delete_success(self, host_cluster, test_namespace):
        """正常删除 - 创建专用资源并删除"""
        # 确保标准资源存在
        if not get_for_test_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleDeleteRuleGroupAPI(
                path_params=HandleDeleteRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=HOST_STANDARD_RULE_GROUP
                ),
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200 

            # 校验返回 message
            data = res.cached_response.raw_response.json()
            assert data.get("message") == "success"
        finally:
            clear_current_cluster()

    def test_delete_not_found(self, host_cluster, test_namespace):
        """删除不存在的规则组"""
        set_current_cluster(host_cluster)
        try:
            api = HandleDeleteRuleGroupAPI(
                path_params=HandleDeleteRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name="nonexistent-group"
                ),
                enable_schema_validation=False,
                response=None
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 404
        finally:
            clear_current_cluster()


# ==================== Member Cluster 多集群测试 ====================

@pytest.mark.alerting_management
@pytest.mark.multi_cluster
class TestNamespaceRuleGroupsMember:
    """Member 集群 - 项目规则组测试"""

    @pytest.fixture(scope="module")
    def cleanup_member_standard(self, member_cluster, test_namespace_member):
        """清理 member 标准资源"""
        yield
        try:
            cleanup_namespace_rule_group(member_cluster, test_namespace_member, MEMBER_STANDARD_RULE_GROUP)
        except Exception as e:
            logger.warning(f"清理 member 标准规则组失败: {e}")

    def test_create_rule_group_on_member(self, member_cluster, test_namespace_member):
        """
        member 集群创建项目规则组
        """
        set_current_cluster(member_cluster)
        try:
            # 从数据文件加载模板并替换占位符
            request_body = load_test_data(
                "whizard_alerting", "Alerting_Management/namespace_rule_groups", "namespace_rule_group_custom"
            )
            request_body["metadata"]["name"] = MEMBER_STANDARD_RULE_GROUP
            request_body["metadata"]["namespace"] = test_namespace_member
            request_body["spec"]["rules"][0]["alert"] = "member-alert"
            request_body["spec"]["rules"][0]["annotations"]["summary"] = "member-summary"

            api = HandleCreateRuleGroupAPI(
                path_params=HandleCreateRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    namespace=test_namespace_member
                ),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            # 校验 owner_cluster 和 owner_namespace 标签
            data = res.cached_response.raw_response.json()
            labels = data.get("metadata", {}).get("labels", {})
            assert labels.get("alerting.kubesphere.io/owner_cluster") == member_cluster
            assert labels.get("alerting.kubesphere.io/owner_namespace") == test_namespace_member
        finally:
            clear_current_cluster()

    def test_list_rule_groups_on_member(self, member_cluster, test_namespace_member, cleanup_member_standard):
        """查看 member 项目规则组列表"""
        # 确保标准资源存在
        if not get_for_test_namespace_rule_group(member_cluster, test_namespace_member, MEMBER_STANDARD_RULE_GROUP):
            pytest.skip("无法在 member 集群创建标准规则组")

        set_current_cluster(member_cluster)
        try:
            api = HandleListRuleGroupsAPI(
                path_params=HandleListRuleGroupsAPI.PathParams(
                    cluster=member_cluster,
                    namespace=test_namespace_member
                ),
                enable_schema_validation=False
            )
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()

            # 校验能查询到 member 标准规则组
            found = any(
                item.get("metadata", {}).get("name") == MEMBER_STANDARD_RULE_GROUP
                for item in (data.get("items") or [])
            )
            assert found, f"未找到 member 标准规则组: {MEMBER_STANDARD_RULE_GROUP}"
        finally:
            clear_current_cluster()

    def test_delete_rule_group_on_member(self, member_cluster, test_namespace_member, cleanup_member_standard):
        """删除 member 项目规则组"""
        # 确保标准资源存在
        if not get_for_test_namespace_rule_group(member_cluster, test_namespace_member, MEMBER_STANDARD_RULE_GROUP):
            pytest.skip("无法在 member 集群创建标准规则组")

        set_current_cluster(member_cluster)
        try:
            api = HandleDeleteRuleGroupAPI(
                path_params=HandleDeleteRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    namespace=test_namespace_member,
                    name=MEMBER_STANDARD_RULE_GROUP
                )
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            # 校验返回 message
            data = res.cached_response.raw_response.json()
            assert data.get("message") == "success"
        finally:
            clear_current_cluster()
