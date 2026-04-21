# -*- coding:utf-8 -*-
"""
全局规则组单接口测试
API: HandleList/Create/Get/Update/Delete/PatchGlobalRuleGroupAPI
"""
import pytest
import time

from apis.whizard_alerting.Alerting_Management.apis import (
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
)
from utils.test_data_helper import load_test_data

TEST_DATA_PATH = "whizard_alerting/Alerting_Management"


@pytest.fixture
def test_rule_group():
    """创建临时规则组，测试后自动清理"""
    group_name = generate_test_name("global-group")

    success = get_for_test_global_rule_group(group_name)
    if not success:
        pytest.skip("无法创建测试规则组")

    yield {"name": group_name}

    cleanup_global_rule_group(group_name)


@pytest.mark.alerting_management
class TestListGlobalRuleGroups:
    """查询全局规则组列表"""

    def test_list_success(self):
        """正常查询列表"""
        api = HandleListGlobalRuleGroupsAPI()
        api.query_params.page = "1"
        api.query_params.ascending = "false"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

    def test_list_with_name_filter(self, test_rule_group):
        """按名称过滤"""
        api = HandleListGlobalRuleGroupsAPI()
        api.query_params.name = test_rule_group["name"]

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

    def test_list_with_state_filter(self):
        """按状态过滤"""
        api = HandleListGlobalRuleGroupsAPI()
        api.query_params.state = "inactive"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200


@pytest.mark.alerting_management
class TestCreateGlobalRuleGroup:
    """创建全局规则组"""

    def test_create_success(self):
        """正常创建"""
        group_name = generate_test_name("global-group")

        request_body = load_test_data("whizard_alerting", "Alerting_Management/global_rule_groups", "test_global_rule_group")
        request_body["metadata"]["name"] = group_name

        api = HandleCreateGlobalRuleGroupAPI(enable_schema_validation=False,
            request_body=request_body
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 201)

        cleanup_global_rule_group(group_name)

    def test_create_with_empty_body(self):
        """空请求体创建 - 应失败"""
        api = HandleCreateGlobalRuleGroupAPI(
            request_body={},
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code >= 400


@pytest.mark.alerting_management
class TestGetGlobalRuleGroup:
    """获取全局规则组详情"""

    def test_get_success(self, test_rule_group):
        """正常获取详情"""
        api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(
                name=test_rule_group["name"]
            )
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == test_rule_group["name"]

    def test_get_not_found(self):
        """获取不存在的规则组"""
        api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(
                name="nonexistent-group"
            ),
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 404)


@pytest.mark.alerting_management
class TestUpdateGlobalRuleGroup:
    """更新全局规则组"""

    def test_update_success(self, test_rule_group):
        """正常更新"""
        request_body = load_test_data("whizard_alerting", "Alerting_Management/global_rule_groups", "test_global_rule_group")
        request_body["metadata"]["name"] = test_rule_group["name"]
        request_body["spec"]["rules"][0]["alert"] = "UpdatedGlobalAlert"

        api = HandleUpdateGlobalRuleGroupAPI(enable_schema_validation=False,
            path_params=HandleUpdateGlobalRuleGroupAPI.PathParams(
                name=test_rule_group["name"]
            ),
            request_body=request_body
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code == 200

    def test_update_not_found(self):
        """更新不存在的规则组"""
        request_body = load_test_data("whizard_alerting", "Alerting_Management/global_rule_groups", "test_global_rule_group")
        request_body["metadata"]["name"] = "nonexistent-group"

        api = HandleUpdateGlobalRuleGroupAPI(
            path_params=HandleUpdateGlobalRuleGroupAPI.PathParams(
                name="nonexistent-group"
            ),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code == 404


@pytest.mark.alerting_management
class TestPatchGlobalRuleGroup:
    """部分更新全局规则组"""

    def test_patch_disabled(self, test_rule_group):
        """禁用规则"""
        request_body = {
            "spec": {
                "rules": [
                    {
                        "disable": True
                    }
                ]
            }
        }

        api = HandlePatchGlobalRuleGroupAPI(
            path_params=HandlePatchGlobalRuleGroupAPI.PathParams(
                name=test_rule_group["name"]
            ),
            request_body=request_body
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code == 200


@pytest.mark.alerting_management
class TestDeleteGlobalRuleGroup:
    """删除全局规则组"""

    def test_delete_success(self):
        """正常删除"""
        group_name = generate_test_name("global-group-del")
        success = get_for_test_global_rule_group(group_name)
        if not success:
            pytest.skip("无法创建待删除的测试规则组")

        api = HandleDeleteGlobalRuleGroupAPI(
            path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(
                name=group_name
            )
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 204)

    def test_delete_not_found(self):
        """删除不存在的规则组"""
        api = HandleDeleteGlobalRuleGroupAPI(
            path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(
                name="nonexistent-group"
            ),
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 404)
