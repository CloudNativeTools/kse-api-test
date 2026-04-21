# -*- coding:utf-8 -*-
"""
命名空间规则组单接口测试
API: HandleList/Create/Get/Update/Delete/PatchRuleGroupAPI
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
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

TEST_DATA_PATH = "whizard_alerting/Alerting_Management"
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def test_namespace():
    return "default"


@pytest.fixture
def test_rule_group(host_cluster, test_namespace):
    """创建临时规则组，测试后自动清理"""
    group_name = generate_test_name("ns-group")

    success = get_for_test_namespace_rule_group(host_cluster, test_namespace, group_name)
    if not success:
        pytest.skip("无法创建测试规则组")

    yield {"cluster": host_cluster, "namespace": test_namespace, "name": group_name}

    cleanup_namespace_rule_group(host_cluster, test_namespace, group_name)


@pytest.mark.alerting_management
class TestListNamespaceRuleGroups:
    """查询命名空间规则组列表"""

    def test_list_success(self, host_cluster, test_namespace):
        """正常查询列表"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListRuleGroupsAPI()
            api.path_params = HandleListRuleGroupsAPI.PathParams(
                cluster=host_cluster,
                namespace=test_namespace
            )
            api.query_params.page = "1"
            api.query_params.ascending = "false"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data
            assert "totalItems" in data
        finally:
            clear_current_cluster()

    def test_list_with_name_filter(self, host_cluster, test_namespace, test_rule_group):
        """按名称过滤"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListRuleGroupsAPI()
            api.path_params = HandleListRuleGroupsAPI.PathParams(
                cluster=host_cluster,
                namespace=test_namespace
            )
            api.query_params.name = test_rule_group["name"]

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()


@pytest.mark.alerting_management
class TestCreateNamespaceRuleGroup:
    """创建命名空间规则组"""

    def test_create_success(self, host_cluster, test_namespace):
        """正常创建"""
        group_name = generate_test_name("ns-group")

        set_current_cluster(host_cluster)
        try:
            request_body = load_test_data("whizard_alerting", "Alerting_Management/namespace_rule_groups", "test_namespace_rule_group")
            request_body["metadata"]["name"] = group_name

            api = HandleCreateRuleGroupAPI(enable_schema_validation=False,
                path_params=HandleCreateRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace
                ),
                request_body=request_body
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 201)

            cleanup_namespace_rule_group(host_cluster, test_namespace, group_name)
        finally:
            clear_current_cluster()

    def test_create_with_empty_body(self, host_cluster, test_namespace):
        """空请求体创建 - 应失败"""
        set_current_cluster(host_cluster)
        try:
            api = HandleCreateRuleGroupAPI(
                path_params=HandleCreateRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace
                ),
                request_body={},
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code >= 400
        finally:
            clear_current_cluster()


@pytest.mark.alerting_management
class TestGetNamespaceRuleGroup:
    """获取命名空间规则组详情"""

    def test_get_success(self, host_cluster, test_namespace, test_rule_group):
        """正常获取详情"""
        set_current_cluster(host_cluster)
        try:
            api = HandleGetRuleGroupAPI(
                path_params=HandleGetRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=test_rule_group["name"]
                )
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == test_rule_group["name"]
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
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 404)
        finally:
            clear_current_cluster()


@pytest.mark.alerting_management
class TestUpdateNamespaceRuleGroup:
    """更新命名空间规则组"""

    def test_update_success(self, host_cluster, test_namespace, test_rule_group):
        """正常更新"""
        set_current_cluster(host_cluster)
        try:
            request_body = load_test_data("whizard_alerting", "Alerting_Management/namespace_rule_groups", "test_namespace_rule_group")
            request_body["metadata"]["name"] = test_rule_group["name"]
            request_body["spec"]["rules"][0]["alert"] = "UpdatedNamespaceAlert"

            api = HandleUpdateRuleGroupAPI(enable_schema_validation=False,
                path_params=HandleUpdateRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=test_rule_group["name"]
                ),
                request_body=request_body
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()


@pytest.mark.alerting_management
class TestPatchNamespaceRuleGroup:
    """部分更新命名空间规则组"""

    def test_patch_disabled(self, host_cluster, test_namespace, test_rule_group):
        """禁用规则"""
        set_current_cluster(host_cluster)
        try:
            request_body = {
                "spec": {
                    "rules": [
                        {
                            "disable": True
                        }
                    ]
                }
            }

            api = HandlePatchRuleGroupAPI(
                path_params=HandlePatchRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=test_rule_group["name"]
                ),
                request_body=request_body
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()


@pytest.mark.alerting_management
class TestDeleteNamespaceRuleGroup:
    """删除命名空间规则组"""

    def test_delete_success(self, host_cluster, test_namespace):
        """正常删除"""
        group_name = generate_test_name("ns-group-del")
        success = get_for_test_namespace_rule_group(host_cluster, test_namespace, group_name)
        if not success:
            pytest.skip("无法创建待删除的测试规则组")

        set_current_cluster(host_cluster)
        try:
            api = HandleDeleteRuleGroupAPI(
                path_params=HandleDeleteRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace,
                    name=group_name
                )
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 204)
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
                enable_schema_validation=False
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 404)
        finally:
            clear_current_cluster()


# ==================== Member Cluster 多集群测试 ====================

@pytest.mark.alerting_management
@pytest.mark.multi_cluster
class TestListNamespaceRuleGroupsMember:
    """Member 集群 - 查询命名空间规则组列表"""

    def test_list_on_member_cluster(self, member_cluster, test_namespace):
        """在 member 集群查询命名空间规则组列表"""
        set_current_cluster(member_cluster)
        try:
            api = HandleListRuleGroupsAPI()
            api.path_params = HandleListRuleGroupsAPI.PathParams(
                cluster=member_cluster,
                namespace=test_namespace
            )
            api.query_params.page = "1"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data
            assert "totalItems" in data
        finally:
            clear_current_cluster()

    def test_list_different_from_host_cluster(self, host_cluster, member_cluster, test_namespace):
        """验证 member 集群和 host 集群返回的数据不同"""
        set_current_cluster(member_cluster)
        try:
            api = HandleListRuleGroupsAPI()
            api.path_params = HandleListRuleGroupsAPI.PathParams(
                cluster=member_cluster,
                namespace=test_namespace
            )
            api.query_params.page = "1"
            res = api.send()
            member_items = res.cached_response.raw_response.json().get("items", [])
            member_names = {item.get("metadata", {}).get("name") for item in member_items}
        finally:
            clear_current_cluster()

        set_current_cluster(host_cluster)
        try:
            api = HandleListRuleGroupsAPI()
            api.path_params = HandleListRuleGroupsAPI.PathParams(
                cluster=host_cluster,
                namespace=test_namespace
            )
            api.query_params.page = "1"
            res = api.send()
            host_items = res.cached_response.raw_response.json().get("items", [])
            host_names = {item.get("metadata", {}).get("name") for item in host_items}
        finally:
            clear_current_cluster()

        logger.info(f"Host 命名空间规则组: {host_names}")
        logger.info(f"Member 命名空间规则组: {member_names}")

    def test_create_on_member_cluster(self, member_cluster, test_namespace):
        """在 member 集群创建命名空间规则组"""
        group_name = generate_test_name("member-ns-group")

        set_current_cluster(member_cluster)
        try:
            request_body = load_test_data("whizard_alerting", "Alerting_Management/namespace_rule_groups", "test_namespace_rule_group")
            request_body["metadata"]["name"] = group_name

            api = HandleCreateRuleGroupAPI(enable_schema_validation=False,
                path_params=HandleCreateRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    namespace=test_namespace
                ),
                request_body=request_body
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 201)

            cleanup_namespace_rule_group(member_cluster, test_namespace, group_name)
        finally:
            clear_current_cluster()

    def test_get_on_member_cluster(self, member_cluster, test_namespace):
        """在 member 集群获取命名空间规则组详情"""
        group_name = generate_test_name("member-ns-group-get")

        success = get_for_test_namespace_rule_group(member_cluster, test_namespace, group_name)
        if not success:
            pytest.skip("无法在 member 集群创建测试规则组")

        set_current_cluster(member_cluster)
        try:
            api = HandleGetRuleGroupAPI(
                path_params=HandleGetRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    namespace=test_namespace,
                    name=group_name
                )
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == group_name
        finally:
            clear_current_cluster()
            cleanup_namespace_rule_group(member_cluster, test_namespace, group_name)

    def test_delete_on_member_cluster(self, member_cluster, test_namespace):
        """在 member 集群删除命名空间规则组"""
        group_name = generate_test_name("member-ns-group-del")
        success = get_for_test_namespace_rule_group(member_cluster, test_namespace, group_name)
        if not success:
            pytest.skip("无法在 member 集群创建待删除的测试规则组")

        set_current_cluster(member_cluster)
        try:
            api = HandleDeleteRuleGroupAPI(
                path_params=HandleDeleteRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    namespace=test_namespace,
                    name=group_name
                )
            )
            res = api.send()

            assert res.cached_response.raw_response.status_code in (200, 204)
        finally:
            clear_current_cluster()
