# -*- coding:utf-8 -*-
"""
whizard-alerting 租户侧权限测试
验证不同角色对告警 API 的访问权限

测试策略：
1. 平台级角色 - 验证全局/集群/项目全部访问能力，以及无企业空间用户无法访问
2. 集群级角色 - 验证集群规则组和告警的权限
3. 企业空间级角色 - 验证项目级规则组和告警的权限
4. 项目级角色 - 验证项目级规则组和告警的权限
"""
import pytest

from apis.whizard_alerting.alerting_management.apis import (
    HandleListGlobalRuleGroupsAPI,
    HandleCreateGlobalRuleGroupAPI,
    HandleGetGlobalRuleGroupAPI,
    HandleDeleteGlobalRuleGroupAPI,
    HandleListClusterRuleGroupsAPI,
    HandleCreateClusterRuleGroupAPI,
    HandleGetClusterRuleGroupAPI,
    HandleUpdateClusterRuleGroupAPI,
    HandleDeleteClusterRuleGroupAPI,
    HandleListRuleGroupsAPI,
    HandleCreateRuleGroupAPI,
    HandleGetRuleGroupAPI,
    HandleUpdateRuleGroupAPI,
    HandleDeleteRuleGroupAPI,
    HandleListGlobalAlertsAPI,
    HandleListClusterAlertsAPI,
    HandleListAlertsAPI,
)
from testcases.test_api.whizard_alerting.base import (
    generate_test_name,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster
from utils.user_switch_helper import UserContext


ACCOUNTS = load_test_data(
    "_common", "permission_accounts"
)


@pytest.fixture(scope="module")
def cleanup_created_rule_groups():
    """跟踪并清理测试中创建的规则组"""
    created_groups = {
        "global": [],
        "cluster": [],
        "namespace": [],
    }
    yield created_groups

    account = ACCOUNTS["pl_admin"]
    with UserContext(account["user"], account["pwd"]):
        for group_name in created_groups["global"]:
            try:
                api = HandleDeleteGlobalRuleGroupAPI(
                    path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(name=group_name),
                    enable_schema_validation=False
                )
                api.send()
            except Exception:
                pass

        for cluster, group_name in created_groups["cluster"]:
            try:
                set_current_cluster(cluster)
                api = HandleDeleteClusterRuleGroupAPI(
                    path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                        cluster=cluster, name=group_name
                    ),
                    enable_schema_validation=False
                )
                api.send()
            except Exception:
                pass
            finally:
                clear_current_cluster()

        for cluster, namespace, group_name in created_groups["namespace"]:
            try:
                set_current_cluster(cluster)
                api = HandleDeleteRuleGroupAPI(
                    path_params=HandleDeleteRuleGroupAPI.PathParams(
                        cluster=cluster, namespace=namespace, name=group_name
                    ),
                    enable_schema_validation=False
                )
                api.send()
            except Exception:
                pass
            finally:
                clear_current_cluster()


@pytest.fixture(scope="module")
def cluster_rule_group_template():
    return load_test_data(
        "whizard_alerting", "alerting_management/cluster_rule_groups", "cluster_rule_group_custom"
    )


@pytest.fixture(scope="module")
def namespace_rule_group_template():
    return load_test_data(
        "whizard_alerting", "alerting_management/namespace_rule_groups", "namespace_rule_group_custom"
    )


@pytest.fixture(scope="module")
def global_rule_group_template():
    return load_test_data(
        "whizard_alerting", "alerting_management/global_rule_groups", "global_rule_group_custom"
    )


# ==================== 平台级角色 ====================

@pytest.mark.alerting_management
@pytest.mark.tenant_permission
class TestTenantPermissionPlatformRole:
    """平台级角色权限验证"""

    def test_pl_admin_access_global(self, global_rule_group_template):
        """pl-admin 可访问全局规则组"""
        account = ACCOUNTS["pl_admin"]
        with UserContext(account["user"], account["pwd"]):
            api = HandleListGlobalRuleGroupsAPI(
                enable_schema_validation=False,
                response=None
            )
            api.query_params.limit = "10"
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

    def test_pl_admin_access_cluster(self, host_cluster, cluster_rule_group_template):
        """pl-admin 可访问集群规则组"""
        account = ACCOUNTS["pl_admin"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListClusterRuleGroupsAPI(
                    path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=host_cluster),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_pl_admin_access_namespace(self, host_cluster, test_namespace, namespace_rule_group_template):
        """pl-admin 可访问项目规则组"""
        account = ACCOUNTS["pl_admin"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListRuleGroupsAPI(
                    path_params=HandleListRuleGroupsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_pl_regular_no_access_global(self):
        """pl-regular 无企业空间，无权访问全局规则组"""
        account = ACCOUNTS["pl_regular"]
        with UserContext(account["user"], account["pwd"]):
            api = HandleListGlobalRuleGroupsAPI(
                enable_schema_validation=False,
                response=None
            )
            api.query_params.limit = "10"
            res = api.send()
            assert res.cached_response.raw_response.status_code in (403, 401)

    def test_pl_regular_no_access_cluster(self, host_cluster):
        """pl-regular 无企业空间，无权访问集群规则组"""
        account = ACCOUNTS["pl_regular"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListClusterRuleGroupsAPI(
                    path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=host_cluster),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code in (403, 401)
            finally:
                clear_current_cluster()

    def test_pl_regular_no_access_namespace(self, host_cluster, test_namespace):
        """pl-regular 无企业空间，无权访问项目规则组"""
        account = ACCOUNTS["pl_regular"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListRuleGroupsAPI(
                    path_params=HandleListRuleGroupsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code in (403, 401)
            finally:
                clear_current_cluster()

    def test_pl_admin_create_global_rule_group(self, global_rule_group_template, cleanup_created_rule_groups):
        """pl-admin 可创建全局规则组"""
        account = ACCOUNTS["pl_admin"]
        group_name = generate_test_name("global-perm")
        with UserContext(account["user"], account["pwd"]):
            request_body = global_rule_group_template.copy()
            request_body["metadata"]["name"] = group_name
            api = HandleCreateGlobalRuleGroupAPI(
                request_body=request_body,
                enable_schema_validation=False
            )
            res = api.send()
            cleanup_created_rule_groups["global"].append(group_name)
            assert res.cached_response.raw_response.status_code in (200, 201)

    def test_pl_admin_get_global_rule_group(self):
        """pl-admin 可查询全局规则组详情"""
        account = ACCOUNTS["pl_admin"]
        with UserContext(account["user"], account["pwd"]):
            api = HandleListGlobalRuleGroupsAPI(
                enable_schema_validation=False,
                response=None
            )
            api.query_params.limit = "1"
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
            items = res.cached_response.json().get("items", [])
            if items:
                group_name = items[0]["metadata"]["name"]
                get_api = HandleGetGlobalRuleGroupAPI(
                    path_params=HandleGetGlobalRuleGroupAPI.PathParams(name=group_name),
                    enable_schema_validation=False,
                    response=None
                )
                get_res = get_api.send()
                assert get_res.cached_response.raw_response.status_code == 200

    def test_pl_admin_list_global_alerts(self):
        """pl-admin 可查询全局告警"""
        account = ACCOUNTS["pl_admin"]
        with UserContext(account["user"], account["pwd"]):
            api = HandleListGlobalAlertsAPI(
                enable_schema_validation=False,
                response=None
            )
            api.query_params.limit = "10"
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

    def test_pl_regular_no_access_global_rule_group(self, global_rule_group_template):
        """pl-regular 无权创建全局规则组"""
        account = ACCOUNTS["pl_regular"]
        with UserContext(account["user"], account["pwd"]):
            request_body = global_rule_group_template.copy()
            request_body["metadata"]["name"] = generate_test_name("global-perm")
            api = HandleCreateGlobalRuleGroupAPI(
                request_body=request_body,
                enable_schema_validation=False,
                response=None
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code in (403, 401)

    def test_pl_regular_no_list_global_alerts(self):
        """pl-regular 无权查询全局告警"""
        account = ACCOUNTS["pl_regular"]
        with UserContext(account["user"], account["pwd"]):
            api = HandleListGlobalAlertsAPI(
                enable_schema_validation=False,
                response=None
            )
            api.query_params.limit = "10"
            res = api.send()
            assert res.cached_response.raw_response.status_code in (403, 401)


# ==================== 集群级角色 ====================

@pytest.mark.alerting_management
@pytest.mark.tenant_permission
class TestTenantPermissionClusterRole:
    """集群级角色权限验证"""

    def test_cluster_admin_list_rule_groups(self, host_cluster):
        """cluster-admin 可查询集群规则组"""
        account = ACCOUNTS["cluster_admin"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListClusterRuleGroupsAPI(
                    path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=host_cluster),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_cluster_admin_create_rule_group(self, host_cluster, cluster_rule_group_template, cleanup_created_rule_groups):
        """cluster-admin 可创建集群规则组"""
        account = ACCOUNTS["cluster_admin"]
        group_name = generate_test_name("cluster-perm")

        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                request_body = cluster_rule_group_template.copy()
                request_body["metadata"]["name"] = group_name

                api = HandleCreateClusterRuleGroupAPI(
                    path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=host_cluster),
                    request_body=request_body,
                    enable_schema_validation=False
                )
                res = api.send()
                cleanup_created_rule_groups["cluster"].append((host_cluster, group_name))
                assert res.cached_response.raw_response.status_code in (200, 201)
            finally:
                clear_current_cluster()

    def test_cluster_admin_read_alerts(self, host_cluster):
        """cluster-admin 可查询集群告警"""
        account = ACCOUNTS["cluster_admin"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListClusterAlertsAPI(
                    path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_cluster_viewer_read_alerts(self, host_cluster):
        """cluster-viewer 可查询集群告警"""
        account = ACCOUNTS["cluster_viewer"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListClusterAlertsAPI(
                    path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_cluster_viewer_cannot_create_rule_group(self, host_cluster, cluster_rule_group_template):
        """cluster-viewer 无权创建集群规则组"""
        account = ACCOUNTS["cluster_viewer"]
        group_name = generate_test_name("cluster-perm")

        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                request_body = cluster_rule_group_template.copy()
                request_body["metadata"]["name"] = group_name

                api = HandleCreateClusterRuleGroupAPI(
                    path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=host_cluster),
                    request_body=request_body,
                    enable_schema_validation=False,
                    response=None
                )
                res = api.send()
                assert res.cached_response.raw_response.status_code in (403, 401)
            finally:
                clear_current_cluster()


# ==================== 企业空间级角色 ====================

@pytest.mark.alerting_management
@pytest.mark.tenant_permission
class TestTenantPermissionWorkspaceRole:
    """企业空间级角色权限验证"""

    def test_ws_admin_list_rule_groups(self, host_cluster, test_namespace):
        """ws-admin 可查询项目规则组"""
        account = ACCOUNTS["ws_admin"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListRuleGroupsAPI(
                    path_params=HandleListRuleGroupsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_ws_admin_create_rule_group(self, host_cluster, test_namespace, namespace_rule_group_template, cleanup_created_rule_groups):
        """ws-admin 可创建项目规则组"""
        account = ACCOUNTS["ws_admin"]
        group_name = generate_test_name("ws-perm")

        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                request_body = namespace_rule_group_template.copy()
                request_body["metadata"]["name"] = group_name
                request_body["metadata"]["namespace"] = test_namespace
                request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"

                api = HandleCreateRuleGroupAPI(
                    path_params=HandleCreateRuleGroupAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    request_body=request_body,
                    enable_schema_validation=False
                )
                res = api.send()
                cleanup_created_rule_groups["namespace"].append((host_cluster, test_namespace, group_name))
                assert res.cached_response.raw_response.status_code in (200, 201)
            finally:
                clear_current_cluster()

    def test_ws_admin_read_alerts(self, host_cluster, test_namespace):
        """ws-admin 可查询项目告警"""
        account = ACCOUNTS["ws_admin"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListAlertsAPI(
                    path_params=HandleListAlertsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_ws_viewer_read_alerts(self, host_cluster, test_namespace):
        """ws-viewer 可查询项目告警"""
        account = ACCOUNTS["ws_viewer"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListAlertsAPI(
                    path_params=HandleListAlertsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_ws_viewer_cannot_create_rule_group(self, host_cluster, test_namespace, namespace_rule_group_template):
        """ws-viewer 无权创建项目规则组"""
        account = ACCOUNTS["ws_viewer"]
        group_name = generate_test_name("ws-perm")

        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                request_body = namespace_rule_group_template.copy()
                request_body["metadata"]["name"] = group_name
                request_body["metadata"]["namespace"] = test_namespace
                request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"

                api = HandleCreateRuleGroupAPI(
                    path_params=HandleCreateRuleGroupAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    request_body=request_body,
                    enable_schema_validation=False,
                    response=None
                )
                res = api.send()
                assert res.cached_response.raw_response.status_code in (403, 401)
            finally:
                clear_current_cluster()


# ==================== 项目级角色 ====================

@pytest.mark.alerting_management
@pytest.mark.tenant_permission
class TestTenantPermissionProjectRole:
    """项目级角色权限验证"""

    def test_pro_admin_list_rule_groups(self, host_cluster, test_namespace):
        """pro-admin 可查询项目规则组"""
        account = ACCOUNTS["pro_admin"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListRuleGroupsAPI(
                    path_params=HandleListRuleGroupsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_pro_admin_create_rule_group(self, host_cluster, test_namespace, namespace_rule_group_template, cleanup_created_rule_groups):
        """pro-admin 可创建项目规则组"""
        account = ACCOUNTS["pro_admin"]
        group_name = generate_test_name("pro-perm")

        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                request_body = namespace_rule_group_template.copy()
                request_body["metadata"]["name"] = group_name
                request_body["metadata"]["namespace"] = test_namespace
                request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"

                api = HandleCreateRuleGroupAPI(
                    path_params=HandleCreateRuleGroupAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    request_body=request_body,
                    enable_schema_validation=False
                )
                res = api.send()
                cleanup_created_rule_groups["namespace"].append((host_cluster, test_namespace, group_name))
                assert res.cached_response.raw_response.status_code in (200, 201)
            finally:
                clear_current_cluster()

    def test_pro_admin_read_alerts(self, host_cluster, test_namespace):
        """pro-admin 可查询项目告警"""
        account = ACCOUNTS["pro_admin"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListAlertsAPI(
                    path_params=HandleListAlertsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_pro_operator_list_rule_groups(self, host_cluster, test_namespace):
        """pro-operator 可查询项目规则组（与 pro-admin 权限相同）"""
        account = ACCOUNTS["pro_operator"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListRuleGroupsAPI(
                    path_params=HandleListRuleGroupsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_pro_operator_create_rule_group(self, host_cluster, test_namespace, namespace_rule_group_template, cleanup_created_rule_groups):
        """pro-operator 可创建项目规则组（与 pro-admin 权限相同）"""
        account = ACCOUNTS["pro_operator"]
        group_name = generate_test_name("pro-op-perm")

        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                request_body = namespace_rule_group_template.copy()
                request_body["metadata"]["name"] = group_name
                request_body["metadata"]["namespace"] = test_namespace
                request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"

                api = HandleCreateRuleGroupAPI(
                    path_params=HandleCreateRuleGroupAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    request_body=request_body,
                    enable_schema_validation=False
                )
                res = api.send()
                cleanup_created_rule_groups["namespace"].append((host_cluster, test_namespace, group_name))
                assert res.cached_response.raw_response.status_code in (200, 201)
            finally:
                clear_current_cluster()

    def test_pro_operator_read_alerts(self, host_cluster, test_namespace):
        """pro-operator 可查询项目告警（与 pro-admin 权限相同）"""
        account = ACCOUNTS["pro_operator"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListAlertsAPI(
                    path_params=HandleListAlertsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_pro_viewer_read_alerts(self, host_cluster, test_namespace):
        """pro-viewer 可查询项目告警"""
        account = ACCOUNTS["pro_viewer"]
        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                api = HandleListAlertsAPI(
                    path_params=HandleListAlertsAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    enable_schema_validation=False,
                    response=None
                )
                api.query_params.limit = "10"
                res = api.send()
                assert res.cached_response.raw_response.status_code == 200
            finally:
                clear_current_cluster()

    def test_pro_viewer_cannot_create_rule_group(self, host_cluster, test_namespace, namespace_rule_group_template):
        """pro-viewer 无权创建项目规则组"""
        account = ACCOUNTS["pro_viewer"]
        group_name = generate_test_name("pro-perm")

        with UserContext(account["user"], account["pwd"]):
            set_current_cluster(host_cluster)
            try:
                request_body = namespace_rule_group_template.copy()
                request_body["metadata"]["name"] = group_name
                request_body["metadata"]["namespace"] = test_namespace
                request_body["spec"]["rules"][0]["alert"] = f"{group_name}-alert"

                api = HandleCreateRuleGroupAPI(
                    path_params=HandleCreateRuleGroupAPI.PathParams(
                        cluster=host_cluster,
                        namespace=test_namespace
                    ),
                    request_body=request_body,
                    enable_schema_validation=False,
                    response=None
                )
                res = api.send()
                assert res.cached_response.raw_response.status_code in (403, 401)
            finally:
                clear_current_cluster()
