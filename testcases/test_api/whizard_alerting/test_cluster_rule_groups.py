# -*- coding:utf-8 -*-
"""
集群规则组单接口测试
API: HandleList/Create/Get/Update/Delete/PatchClusterRuleGroupAPI

测试策略：
1. 使用标准资源（固定名称）贯穿所有接口测试
2. get_for_test 确保资源存在（查不到就创建）
3. 创建接口单独测试（创建新资源，不带删除）
4. 模块级 cleanup 兜底清理
"""
import pytest
import logging

from apis.whizard_alerting.Alerting_Management.apis import (
    HandleListClusterRuleGroupsAPI,
    HandleCreateClusterRuleGroupAPI,
    HandleGetClusterRuleGroupAPI,
    HandleUpdateClusterRuleGroupAPI,
    HandleDeleteClusterRuleGroupAPI,
    HandlePatchClusterRuleGroupAPI
)
from testcases.test_api.whizard_alerting.base import (
    get_for_test_cluster_rule_group,
    cleanup_cluster_rule_group,
    generate_test_name,
    build_patch_body_for_alias_desc,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

TEST_DATA_PATH = "whizard_alerting/Alerting_Management"
logger = logging.getLogger(__name__)

# 标准资源名称（固定，不带时间戳）
STANDARD_RULE_GROUP = "cluster-alert-standard"

@pytest.fixture(scope="module")
def cleanup_standard_rule_group(host_cluster):
    """模块级清理：清理标准资源"""
    yield
    
    # 模块结束后清理标准资源
    logger.info(f"清理标准规则组: {STANDARD_RULE_GROUP}")
    try:
        cleanup_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP)
    except Exception as e:
        logger.warning(f"清理标准规则组失败: {e}")


# ==================== Create ====================

@pytest.mark.alerting_management
class TestCreateClusterRuleGroup:
    """创建集群规则组 - 创建新资源（带时间戳），类级别统一清理"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_created_groups(self, host_cluster):
        """
        类级别 fixture：收集测试创建的资源名，统一清理
        """
        created_groups = []  # 收集创建的资源名
        yield created_groups
        
        # 类中所有测试执行完毕后，统一清理
        logger.info(f"开始清理创建的资源: {created_groups}")
        for group_name in created_groups:
            try:
                set_current_cluster(host_cluster)
                cleanup_cluster_rule_group(host_cluster, group_name)
                clear_current_cluster()
                logger.info(f"已清理: {group_name}")
            except Exception as e:
                logger.warning(f"清理失败 {group_name}: {e}")

    def test_create_template_rule_group(self, host_cluster, cleanup_created_groups):
        """
        创建集群模板规则组（使用 exprBuilder） // TODO: 需补充查询当前节点前置条件
        """
        group_name = generate_test_name("cluster-alert")

        set_current_cluster(host_cluster)
        try:
            # 1. 创建规则组
            request_body = load_test_data(
                "whizard_alerting", "Alerting_Management/cluster_rule_groups", "cluster_rule_group_template"
            )
            request_body["metadata"]["name"] = group_name

            api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=host_cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            # 2. 验证响应状态码
            assert res.cached_response.raw_response.status_code in (200, 201), \
                f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

            # 3. 验证返回数据
            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == group_name, \
                f"返回的 name 不匹配: {data.get('metadata', {}).get('name')} != {group_name}"
            assert "spec" in data and "rules" in data["spec"], \
                "返回数据缺少 spec.rules"
            assert len(data["spec"]["rules"]) > 0, \
                "规则列表为空"

            # 4. 记录创建的资源名，供 fixture 清理
            cleanup_created_groups.append(group_name)
            logger.info(f"模板规则组创建成功: {group_name}")
        finally:
            clear_current_cluster()

    def test_create_custom_rule_group(self, host_cluster, cleanup_created_groups):
        """
        创建集群自定义规则组（使用 expr）
        验证点：
        1. 创建成功（200/201）
        2. 返回的 metadata.name 正确
        3. 返回的 spec.rules[].expr 正确（vector(1)）
        """
        group_name = generate_test_name("cluster-custom-alert")

        set_current_cluster(host_cluster)
        try:
            # 1. 创建规则组
            request_body = load_test_data(
                "whizard_alerting", "Alerting_Management/cluster_rule_groups", "cluster_rule_group_custom"
            )
            request_body["metadata"]["name"] = group_name

            api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=host_cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            # 2. 验证响应状态码
            assert res.cached_response.raw_response.status_code in (200, 201), \
                f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

            # 3. 验证返回数据
            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == group_name, \
                f"返回的 name 不匹配: {data.get('metadata', {}).get('name')} != {group_name}"
            assert "spec" in data and "rules" in data["spec"], \
                "返回数据缺少 spec.rules"
            
            # 验证 expr 是 vector(1)（自定义规则组的特征）
            rules = data["spec"]["rules"]
            assert len(rules) > 0, "规则列表为空"
            assert rules[0].get("expr") == "vector(1)", \
                f"自定义规则组的 expr 不正确: {rules[0].get('expr')}"

            # 4. 记录创建的资源名，供 fixture 清理
            cleanup_created_groups.append(group_name)
            logger.info(f"自定义规则组创建成功: {group_name}")
        finally:
            clear_current_cluster()


# ==================== List ====================

@pytest.mark.alerting_management
class TestListClusterRuleGroups:
    """查询集群规则组列表"""

    def test_list_success(self, host_cluster, cleanup_standard_rule_group):
        """
        正常查询列表
        先用 get_for_test 确保标准资源存在
        """
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterRuleGroupsAPI(
                path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=host_cluster)
            )
            api.query_params.page = None
            api.query_params.limit = "10"
            api.query_params.ascending = None
            api.query_params.builtin = "false"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data
            assert "totalItems" in data
        finally:
            clear_current_cluster()

    def test_list_with_name_filter(self, host_cluster, cleanup_standard_rule_group):
        """按名称过滤 - 查询标准资源"""
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterRuleGroupsAPI(
                path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=host_cluster)
            )
            api.query_params.name = STANDARD_RULE_GROUP
            api.query_params.page = 1
            api.query_params.limit = "10"
            api.query_params.ascending = None
            api.query_params.builtin = "false"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            # 应该能查到标准资源
            found = any(
                item.get("metadata", {}).get("name") == STANDARD_RULE_GROUP 
                for item in data.get("items", [])
            )
            assert found, f"未找到标准规则组: {STANDARD_RULE_GROUP}"
        finally:
            clear_current_cluster()


# ==================== Get ====================

@pytest.mark.alerting_management
class TestGetClusterRuleGroup:
    """获取集群规则组详情"""

    def test_get_success(self, host_cluster, cleanup_standard_rule_group):
        """查看规则组详情 - 使用标准资源"""
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP
                ),
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == STANDARD_RULE_GROUP
        finally:
            clear_current_cluster()

    def test_get_not_found(self, host_cluster):
        """获取不存在的规则组"""
        set_current_cluster(host_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name="nonexistent-group"
                ),
                enable_schema_validation=False,
                response=None  # 禁用响应体解析
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 404
        finally:
            clear_current_cluster()


# ==================== Update ====================

@pytest.mark.alerting_management
class TestUpdateClusterRuleGroup:
    """更新集群规则组"""

    def test_update_success(self, host_cluster, cleanup_standard_rule_group):
        """修改规则组 - 使用标准资源"""
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            # 1. 先 GET 获取当前规则组完整数据（包含 resourceVersion）
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP
                ),
                enable_schema_validation=False
            )
            get_res = get_api.send()
            current_data = get_res.cached_response.raw_response.json()

            # 2. 修改 annotations
            current_data["spec"]["rules"][0]["annotations"] = {
                "summary": "custom alert info-modify",
                "message": "desc modify"
            }

            # 3. 发送更新请求
            api = HandleUpdateClusterRuleGroupAPI(
                path_params=HandleUpdateClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP
                ),
                request_body=current_data,
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()

    def test_update_not_found(self, host_cluster):
        """更新不存在的规则组"""
        set_current_cluster(host_cluster)
        try:
            request_body = load_test_data(
                "whizard_alerting", "Alerting_Management/cluster_rule_groups", "cluster_rule_group_updated"
            )
            request_body["metadata"]["name"] = "nonexistent-group"

            api = HandleUpdateClusterRuleGroupAPI(
                path_params=HandleUpdateClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name="nonexistent-group"
                ),
                request_body=request_body,
                enable_schema_validation=False,
                response=None  # 禁用响应体解析
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 404
        finally:
            clear_current_cluster()


# ==================== Patch ====================

@pytest.mark.alerting_management
class TestPatchClusterRuleGroup:
    """部分更新集群规则组（Patch）"""

    def test_patch_disabled(self, host_cluster, cleanup_standard_rule_group):
        """
        禁用规则组
        场景：通过 Patch 禁用规则组（修改 metadata.labels.enable）
        """
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            # 构建 Patch 请求体 - 禁用规则组
            request_body = {
                "metadata": {
                    "labels": {
                        "alerting.kubesphere.io/enable": "false"
                    }
                }
            }

            api = HandlePatchClusterRuleGroupAPI(
                path_params=HandlePatchClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP
                ),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            # 验证规则组已被禁用
            data = res.cached_response.raw_response.json()
            labels = data.get("metadata", {}).get("labels", {})
            assert labels.get("alerting.kubesphere.io/enable") == "false", "规则组应已被禁用"
        finally:
            clear_current_cluster()

    def test_patch_edit_alias_and_description(self, host_cluster, cleanup_standard_rule_group):
        """
        编辑规则组别名和描述
        场景：通过 Patch 修改 metadata.annotations 中的 alias-name 和 description
        """
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            # 1. 先 GET 获取当前规则组完整数据
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP
                ),
                enable_schema_validation=False
            )
            get_res = get_api.send()
            current_data = get_res.cached_response.raw_response.json()

            # 2. 使用公共方法构建 Patch 请求体
            request_body = build_patch_body_for_alias_desc(
                current_data=current_data,
                alias_name="updated-alias-name",
                description="updated-description"
            )

            # 3. 发送 Patch 请求
            api = HandlePatchClusterRuleGroupAPI(
                path_params=HandlePatchClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP
                ),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            # 4. 验证别名和描述已更新
            data = res.cached_response.raw_response.json()
            annotations = data.get("metadata", {}).get("annotations", {})
            assert annotations.get("kubesphere.io/alias-name") == "updated-alias-name", "别名应已更新"
            assert annotations.get("kubesphere.io/description") == "updated-description", "描述应已更新"
        finally:
            clear_current_cluster()


# ==================== Delete ====================

@pytest.mark.alerting_management
class TestDeleteClusterRuleGroup:
    """删除集群规则组"""

    def test_delete_success(self, host_cluster):
        """
        删除规则组 - 创建专用资源并删除
        """
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleDeleteClusterRuleGroupAPI(
                path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP
                )
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 204)
        finally:
            clear_current_cluster()

    def test_delete_not_found(self, host_cluster):
        """删除不存在的规则组"""
        set_current_cluster(host_cluster)
        try:
            api = HandleDeleteClusterRuleGroupAPI(
                path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name="nonexistent-group"
                ),
                enable_schema_validation=False,
                response=None  # 禁用响应体解析
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 404)
        finally:
            clear_current_cluster()


# ==================== Member Cluster 多集群测试 ====================

# Member 集群标准资源名称
MEMBER_STANDARD_RULE_GROUP = "member-cluster-alert-standard"


@pytest.mark.alerting_management
@pytest.mark.multi_cluster
class TestClusterRuleGroupsMember:
    """Member 集群 - 集群规则组测试"""

    @pytest.fixture(scope="module")
    def cleanup_member_standard(self, member_cluster):
        """清理 member 标准资源"""
        yield
        try:
            cleanup_cluster_rule_group(member_cluster, MEMBER_STANDARD_RULE_GROUP)
        except Exception as e:
            logger.warning(f"清理 member 标准规则组失败: {e}")

    def test_create_rule_group_on_member(self, member_cluster):
        """
        在 member 集群创建规则组
        校验返回 body：metadata.labels.alerting.kubesphere.io/owner_cluster: "member-cluster"
        """
        set_current_cluster(member_cluster)
        try:
            request_body = load_test_data(
                "whizard_alerting", "Alerting_Management/cluster_rule_groups", "cluster_rule_group_custom"
            )
            request_body["metadata"]["name"] = MEMBER_STANDARD_RULE_GROUP

            api = HandleCreateClusterRuleGroupAPI(enable_schema_validation=False,
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=member_cluster),
                request_body=request_body
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 201)

            # 校验 owner_cluster 标签
            data = res.cached_response.raw_response.json()
            labels = data.get("metadata", {}).get("labels", {})
            assert labels.get("alerting.kubesphere.io/owner_cluster") == member_cluster
        finally:
            clear_current_cluster()

    def test_list_rule_groups_on_member(self, member_cluster):
        """查看 member 规则组列表"""
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(member_cluster, MEMBER_STANDARD_RULE_GROUP):
            pytest.skip("无法在 member 集群创建标准规则组")

        set_current_cluster(member_cluster)
        try:
            api = HandleListClusterRuleGroupsAPI(
                path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=member_cluster)
            )
            api.query_params.page = 1
            api.query_params.limit = "10"
            api.query_params.builtin = "false"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data
        finally:
            clear_current_cluster()

    def test_delete_rule_group_on_member(self, member_cluster):
        """
        删除 member 规则组
        返回 body：{"message": "success"}
        """
        # 确保标准资源存在
        if not get_for_test_cluster_rule_group(member_cluster, MEMBER_STANDARD_RULE_GROUP):
            pytest.skip("无法在 member 集群创建标准规则组")

        set_current_cluster(member_cluster)
        try:
            api = HandleDeleteClusterRuleGroupAPI(
                path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=MEMBER_STANDARD_RULE_GROUP
                )
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 204)
            
            # 校验返回 message
            data = res.cached_response.raw_response.json()
            assert data.get("message") == "success"
        finally:
            clear_current_cluster()
