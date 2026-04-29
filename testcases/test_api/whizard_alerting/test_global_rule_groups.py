# -*- coding:utf-8 -*-
"""
全局规则组单接口测试
API: HandleList/Create/Get/Update/Delete/PatchGlobalRuleGroupAPI

测试策略：
1. 使用标准资源（固定名称）贯穿所有接口测试
2. get_for_test 确保资源存在（查不到就创建）
3. 创建接口单独测试（创建新资源，类级别统一清理）
4. 模块级 cleanup 兜底清理
5. 全局规则组是Global级别，不区分多集群（但规则组内容可包含多集群资源）
"""
import pytest
from loguru import logger

from apis.whizard_alerting.alerting_management.apis import (
    HandleListGlobalRuleGroupsAPI,
    HandleCreateGlobalRuleGroupAPI,
    HandleGetGlobalRuleGroupAPI,
    HandleUpdateGlobalRuleGroupAPI,
    HandleDeleteGlobalRuleGroupAPI,
    HandlePatchGlobalRuleGroupAPI,
)
from testcases.test_api.whizard_alerting.base import (
    get_for_test_global_rule_group,
    cleanup_global_rule_group,
    generate_test_name,
    build_patch_body_for_alias_desc,
    build_update_body_for_rules_annotations,
    build_rule_group_body,
    load_alerting_test_data,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import get_clusters

# 标准资源名称（固定，不带时间戳）
STANDARD_RULE_GROUP = "global-alert-standard"
STANDARD_RULE_GROUP_MULTI = "global-alert-multi"


@pytest.fixture(scope="module")
def cleanup_standard():
    """模块级 fixture：标准资源由 after_all 统一清理，此处不做清理"""
    yield


@pytest.fixture(scope="session")
def has_member_cluster():
    """判断是否为多集群环境"""
    _, member = get_clusters()
    return member is not None


# ==================== Create ====================

@pytest.mark.alerting_management
class TestCreateGlobalRuleGroup:
    """创建全局规则组 - 创建新资源（带时间戳），类级别统一清理"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_created_groups(self):
        """类级别 fixture：收集测试创建的资源名，统一清理"""
        created_groups = []
        yield created_groups

        for group_name in created_groups:
            try:
                cleanup_global_rule_group(group_name)
            except Exception as e:
                logger.warning(f"清理失败 {group_name}: {e}")

    def test_create_template_node_single(self, cleanup_created_groups):
        """
        创建全局模板规则组（单集群-节点）
        验证点：只包含 host 集群节点
        """
        group_name = generate_test_name("global-node-single")

        request_body = load_alerting_test_data(
            "alerting_management/global_rule_groups", "global_rule_group_template_node_single"
        )
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = group_name

        api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == group_name
        assert "exprBuilder" in data["spec"]["rules"][0]
        assert "node" in data["spec"]["rules"][0]["exprBuilder"]

        cleanup_created_groups.append(group_name)
        logger.info(f"单集群节点规则组创建成功: {group_name}")

    @pytest.mark.multi_cluster
    def test_create_template_node_multi(self, cleanup_created_groups, has_member_cluster):
        """
        创建全局模板规则组（多集群-节点）
        验证点：同时包含 host 和 member 集群节点
        """
        if not has_member_cluster:
            pytest.skip("单集群环境跳过")

        group_name = generate_test_name("global-node-multi")

        request_body = load_alerting_test_data(
            "alerting_management/global_rule_groups", "global_rule_group_template_node_multi"
        )
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = group_name

        api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == group_name
        assert "exprBuilder" in data["spec"]["rules"][0]
        assert "node" in data["spec"]["rules"][0]["exprBuilder"]

        cleanup_created_groups.append(group_name)
        logger.info(f"多集群节点规则组创建成功: {group_name}")

    def test_create_template_workload_single(self, cleanup_created_groups):
        """
        创建全局模板规则组（单集群-工作负载）
        验证点：只包含 host 集群工作负载
        """
        group_name = generate_test_name("global-workload-single")

        request_body = load_alerting_test_data(
            "alerting_management/global_rule_groups", "global_rule_group_template_workload_single"
        )
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = group_name

        api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == group_name
        assert "exprBuilder" in data["spec"]["rules"][0]
        assert "workload" in data["spec"]["rules"][0]["exprBuilder"]

        cleanup_created_groups.append(group_name)
        logger.info(f"单集群工作负载规则组创建成功: {group_name}")

    @pytest.mark.multi_cluster
    def test_create_template_workload_multi(self, cleanup_created_groups, has_member_cluster):
        """
        创建全局模板规则组（多集群-工作负载）
        验证点：同时包含 host 和 member 集群工作负载
        """
        if not has_member_cluster:
            pytest.skip("单集群环境跳过")

        group_name = generate_test_name("global-workload-multi")

        request_body = load_alerting_test_data(
            "alerting_management/global_rule_groups", "global_rule_group_template_workload_multi"
        )
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = group_name

        api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == group_name
        assert "exprBuilder" in data["spec"]["rules"][0]
        assert "workload" in data["spec"]["rules"][0]["exprBuilder"]

        cleanup_created_groups.append(group_name)
        logger.info(f"多集群工作负载规则组创建成功: {group_name}")

    def test_create_custom_rule_group(self, cleanup_created_groups):
        """
        创建全局自定义规则组（使用 expr: vector(1)）
        验证点：
        1. 创建成功（200/201）
        2. 返回的 metadata.name 正确
        3. 返回的 spec.rules[].expr = vector(1)
        """
        group_name = generate_test_name("global-custom")

        request_body = load_test_data(
            "whizard_alerting", "alerting_management/global_rule_groups", "global_rule_group_custom"
        )
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"

        api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == group_name
        assert "spec" in data and "rules" in data["spec"]
        rules = data["spec"]["rules"]
        assert len(rules) > 0
        assert rules[0].get("expr") == "vector(1)", f"自定义规则组的 expr 不正确: {rules[0].get('expr')}"

        cleanup_created_groups.append(group_name)
        logger.info(f"自定义规则组创建成功: {group_name}")


# ==================== List ====================

@pytest.mark.alerting_management
class TestListGlobalRuleGroups:
    """查询全局规则组列表"""

    def test_list_all_success(self, cleanup_standard):
        """正常查询列表"""
        if not get_for_test_global_rule_group(STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        api = HandleListGlobalRuleGroupsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

        # 校验规则组条数 > 0，且标准资源组存在于列表中
        items = data.get("items") or []
        total = data.get("totalItems", 0)
        assert total > 0, f"规则组数量应 >0，实际: {total}"

        found = any(item.get("metadata", {}).get("name") == STANDARD_RULE_GROUP for item in items)
        assert found, f"标准规则组 {STANDARD_RULE_GROUP} 应存在于列表中"

    def test_list_custom_rule_groups(self, cleanup_standard):
        """查询自定义规则组列表 (builtin=false)"""
        if not get_for_test_global_rule_group(STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        api = HandleListGlobalRuleGroupsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.builtin = "false"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

        # 校验规则组条数 > 0，且标准资源组存在于列表中
        items = data.get("items") or []
        total = data.get("totalItems", 0)
        assert total > 0, f"自定义规则组数量应 >0，实际: {total}"

        found = any(item.get("metadata", {}).get("name") == STANDARD_RULE_GROUP for item in items)
        assert found, f"标准规则组 {STANDARD_RULE_GROUP} 应存在于自定义规则组列表中"

    def test_list_builtin_rule_groups(self):
        """查询内置规则组列表 (builtin=true)"""
        api = HandleListGlobalRuleGroupsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.builtin = "true"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

        # 校验：totalItems>=1; 且任意规则组的 metadata.labels.alerting.kubesphere.io/builtin: "true"
        total = data.get("totalItems", 0)
        assert total >= 1, f"内置规则组数量应 >=1，实际: {total}"

        items = data.get("items") or []
        has_builtin = any(
            item.get("metadata", {}).get("labels", {}).get("alerting.kubesphere.io/builtin") == "true"
            for item in items
        )
        assert has_builtin, "应存在内置规则组 (alerting.kubesphere.io/builtin=true)"

    def test_list_with_name_filter(self, cleanup_standard):
        """按名称过滤 - 查询标准资源"""
        if not get_for_test_global_rule_group(STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        api = HandleListGlobalRuleGroupsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.name = STANDARD_RULE_GROUP
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        found = any(
            item.get("metadata", {}).get("name") == STANDARD_RULE_GROUP
            for item in (data.get("items") or [])
        )
        assert found, f"未找到标准规则组: {STANDARD_RULE_GROUP}"


# ==================== Get ====================

@pytest.mark.alerting_management
class TestGetGlobalRuleGroup:
    """获取全局规则组详情"""

    def test_get_success(self, cleanup_standard):
        """查看规则组详情 - 使用标准资源"""
        if not get_for_test_global_rule_group(STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(
                name=STANDARD_RULE_GROUP
            ),
            enable_schema_validation=False,
            response=None
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == STANDARD_RULE_GROUP

    def test_get_not_found(self):
        """获取不存在的规则组"""
        api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(
                name="nonexistent-group"
            ),
            enable_schema_validation=False,
            response=None
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code == 404


# ==================== Update ====================

@pytest.mark.alerting_management
class TestUpdateGlobalRuleGroup:
    """更新全局规则组 (PUT)"""

    def test_update_success(self, cleanup_standard):
        """修改规则组 - 使用标准资源"""
        if not get_for_test_global_rule_group(STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        get_api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(
                name=STANDARD_RULE_GROUP
            ),
            enable_schema_validation=False
        )
        get_res = get_api.send()
        current_data = get_res.cached_response.raw_response.json()

        request_body = build_update_body_for_rules_annotations(
            current_data=current_data,
            summary="updated-global-alert-summary",
            message="updated desc"
        )

        api = HandleUpdateGlobalRuleGroupAPI(
            path_params=HandleUpdateGlobalRuleGroupAPI.PathParams(
                name=STANDARD_RULE_GROUP
            ),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        annotations = data.get("spec", {}).get("rules", [{}])[0].get("annotations", {})
        assert annotations.get("summary") == "updated-global-alert-summary", "summary 应已更新"
        assert annotations.get("message") == "updated desc", "message 应已更新"

    def test_reset_builtin_rule_group(self):
        """
        重置全局内置规则组
        1. 先 list 获取内置规则组
        2. 选择第一个内置规则组进行重置（使用其原始数据）
        """
        # 1. 获取内置规则组列表
        list_api = HandleListGlobalRuleGroupsAPI(
            enable_schema_validation=False,
            response=None
        )
        list_api.query_params.builtin = "true"
        list_api.query_params.limit = "10"
        list_api.query_params.sortBy = "createTime"

        res = list_api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        items = data.get("items") or []

        if not items:
            pytest.skip("无内置规则组")

        # 2. 选择第一个内置规则组
        first_group = items[0]
        group_name = first_group.get("metadata", {}).get("name")

        # 3. 获取完整数据进行重置
        get_api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(name=group_name),
            enable_schema_validation=False
        )
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code == 200

        current_data = get_res.cached_response.raw_response.json()

        # 4. 使用公共方法构建重置请求体（移除不必要的字段，保留resourceVersion）
        reset_body = build_rule_group_body(
            current_data=current_data,
            target="spec_rules",
            remove_resource_version=False
        )

        # 5. 发送重置请求
        update_api = HandleUpdateGlobalRuleGroupAPI(
            path_params=HandleUpdateGlobalRuleGroupAPI.PathParams(name=group_name),
            request_body=reset_body,
            enable_schema_validation=False
        )
        update_res = update_api.send()
        assert update_res.cached_response.raw_response.status_code == 200


# ==================== Patch ====================

@pytest.mark.alerting_management
class TestPatchGlobalRuleGroup:
    """部分更新全局规则组 (Patch)"""

    def test_patch_edit_alias_and_description(self, cleanup_standard):
        """
        编辑规则组别名和描述
        场景：通过 Patch 修改 metadata.annotations 中的 alias-name 和 description
        """
        if not get_for_test_global_rule_group(STANDARD_RULE_GROUP):
            pytest.skip("无法创建标准规则组")

        get_api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(
                name=STANDARD_RULE_GROUP
            ),
            enable_schema_validation=False
        )
        get_res = get_api.send()
        current_data = get_res.cached_response.raw_response.json()

        request_body = build_patch_body_for_alias_desc(
            current_data=current_data,
            alias_name="global-alias-updated",
            description="global-desc-updated"
        )

        api = HandlePatchGlobalRuleGroupAPI(
            path_params=HandlePatchGlobalRuleGroupAPI.PathParams(
                name=STANDARD_RULE_GROUP
            ),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        annotations = data.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "global-alias-updated", "别名应已更新"
        assert annotations.get("kubesphere.io/description") == "global-desc-updated", "描述应已更新"


# ==================== Delete ====================

@pytest.mark.alerting_management
class TestDeleteGlobalRuleGroup:
    """删除全局规则组"""

    def test_delete_success(self):
        """正常删除 - 创建临时规则组并删除"""
        group_name = generate_test_name("global-delete")

        request_body = load_test_data(
            "whizard_alerting", "alerting_management/global_rule_groups", "global_rule_group_custom"
        )
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"

        create_api = HandleCreateGlobalRuleGroupAPI(request_body=request_body, enable_schema_validation=False)
        create_res = create_api.send()

        if create_res.cached_response.raw_response.status_code not in (200, 201):
            pytest.skip(f"无法创建待删除的测试规则组: {group_name}")

        try:
            api = HandleDeleteGlobalRuleGroupAPI(
                path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(name=group_name)
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 204)

            data = res.cached_response.raw_response.json()
            assert data.get("message") == "success"
        finally:
            cleanup_global_rule_group(group_name)

    def test_delete_not_found(self):
        """删除不存在的规则组"""
        api = HandleDeleteGlobalRuleGroupAPI(
            path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(
                name="nonexistent-group"
            ),
            enable_schema_validation=False,
            response=None
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code == 404
