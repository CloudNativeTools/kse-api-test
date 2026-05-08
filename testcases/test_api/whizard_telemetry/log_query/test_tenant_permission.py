# -*- coding:utf-8 -*-
"""
whizard-logs 租户侧权限测试
验证不同角色对日志查询 API 的访问权限

测试策略：
1. 平台级角色 - pl-admin 有权访问，pl-regular 无企业空间无权访问
2. 集群级角色 - cluster-admin/cluster-viewer 均可读取
3. 企业空间级角色 - ws-admin/ws-viewer 均可读取
4. 项目级角色 - pro-admin/pro-operator/pro-viewer 均可读取
"""
import pytest

from utils.test_data_helper import load_test_data
from utils.user_switch_helper import UserContext

from testcases.test_api.whizard_telemetry.log_query.base import (
    query_logs_statistics,
    query_logs_histogram,
    query_logs,
)

ACCOUNTS = load_test_data("_common", "permission_accounts")


# ==================== 平台级角色 ====================

@pytest.mark.whizard_logs
@pytest.mark.tenant_permission
class TestTenantPermissionPlatformRole:
    """平台级角色权限验证"""

    def test_pl_admin_query_logs_statistics(self):
        """pl-admin 可查询日志统计"""
        account = ACCOUNTS["pl_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200

    def test_pl_admin_query_logs_histogram(self):
        """pl-admin 可查询日志直方图"""
        account = ACCOUNTS["pl_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200

    def test_pl_admin_query_logs(self):
        """pl-admin 可查询日志列表"""
        account = ACCOUNTS["pl_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200

    def test_pl_regular_no_access_statistics(self):
        """pl-regular 无企业空间，不可见日志统计数据"""
        account = ACCOUNTS["pl_regular"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200
            data = res.cached_response.raw_response.json()
            assert data["statistics"]["logs"] == 0
            assert data["statistics"]["containers"] == 0

    def test_pl_regular_no_access_histogram(self):
        """pl-regular 无企业空间，不可见日志直方图数据"""
        account = ACCOUNTS["pl_regular"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200
            data = res.cached_response.raw_response.json()
            assert data["histogram"]["total"] == 0

    def test_pl_regular_no_access_query(self):
        """pl-regular 无企业空间，不可见日志列表数据"""
        account = ACCOUNTS["pl_regular"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200
            data = res.cached_response.raw_response.json()
            assert data["query"]["total"] == 0


# ==================== 集群级角色 ====================

@pytest.mark.whizard_logs
@pytest.mark.tenant_permission
class TestTenantPermissionClusterRole:
    """集群级角色权限验证"""

    def test_cluster_admin_query_statistics(self):
        """cluster-admin 可查询日志统计"""
        account = ACCOUNTS["cluster_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200

    def test_cluster_admin_query_histogram(self):
        """cluster-admin 可查询日志直方图"""
        account = ACCOUNTS["cluster_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200

    def test_cluster_admin_query_logs(self):
        """cluster-admin 可查询日志列表"""
        account = ACCOUNTS["cluster_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200

    def test_cluster_viewer_query_statistics(self):
        """cluster-viewer 可查询日志统计"""
        account = ACCOUNTS["cluster_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200

    def test_cluster_viewer_query_histogram(self):
        """cluster-viewer 可查询日志直方图"""
        account = ACCOUNTS["cluster_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200

    def test_cluster_viewer_query_logs(self):
        """cluster-viewer 可查询日志列表"""
        account = ACCOUNTS["cluster_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200


# ==================== 企业空间级角色 ====================

@pytest.mark.whizard_logs
@pytest.mark.tenant_permission
class TestTenantPermissionWorkspaceRole:
    """企业空间级角色权限验证"""

    def test_ws_admin_query_statistics(self):
        """ws-admin 可查询日志统计"""
        account = ACCOUNTS["ws_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200

    def test_ws_admin_query_histogram(self):
        """ws-admin 可查询日志直方图"""
        account = ACCOUNTS["ws_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200

    def test_ws_admin_query_logs(self):
        """ws-admin 可查询日志列表"""
        account = ACCOUNTS["ws_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200

    def test_ws_viewer_query_statistics(self):
        """ws-viewer 可查询日志统计"""
        account = ACCOUNTS["ws_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200

    def test_ws_viewer_query_histogram(self):
        """ws-viewer 可查询日志直方图"""
        account = ACCOUNTS["ws_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200

    def test_ws_viewer_query_logs(self):
        """ws-viewer 可查询日志列表"""
        account = ACCOUNTS["ws_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200


# ==================== 项目级角色 ====================

@pytest.mark.whizard_logs
@pytest.mark.tenant_permission
class TestTenantPermissionProjectRole:
    """项目级角色权限验证"""

    def test_pro_admin_query_statistics(self):
        """pro-admin 可查询日志统计"""
        account = ACCOUNTS["pro_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200

    def test_pro_admin_query_histogram(self):
        """pro-admin 可查询日志直方图"""
        account = ACCOUNTS["pro_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200

    def test_pro_admin_query_logs(self):
        """pro-admin 可查询日志列表"""
        account = ACCOUNTS["pro_admin"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200

    def test_pro_operator_query_statistics(self):
        """pro-operator 可查询日志统计"""
        account = ACCOUNTS["pro_operator"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200

    def test_pro_operator_query_histogram(self):
        """pro-operator 可查询日志直方图"""
        account = ACCOUNTS["pro_operator"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200

    def test_pro_operator_query_logs(self):
        """pro-operator 可查询日志列表"""
        account = ACCOUNTS["pro_operator"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200

    def test_pro_viewer_query_statistics(self):
        """pro-viewer 可查询日志统计"""
        account = ACCOUNTS["pro_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_statistics()
            assert res.cached_response.raw_response.status_code == 200

    def test_pro_viewer_query_histogram(self):
        """pro-viewer 可查询日志直方图"""
        account = ACCOUNTS["pro_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs_histogram()
            assert res.cached_response.raw_response.status_code == 200

    def test_pro_viewer_query_logs(self):
        """pro-viewer 可查询日志列表"""
        account = ACCOUNTS["pro_viewer"]
        with UserContext(account["user"], account["pwd"]):
            res = query_logs()
            assert res.cached_response.raw_response.status_code == 200