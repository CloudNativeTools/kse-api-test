# -*- coding:utf-8 -*-
"""
命名空间告警列表单接口测试
API: HandleListAlertsAPI
"""
import pytest
import logging

from apis.whizard_alerting.Alerting_Management.apis import HandleListAlertsAPI
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

logger = logging.getLogger(__name__)


@pytest.mark.alerting_management
class TestListNamespaceAlerts:
    """查询命名空间告警列表"""

    def test_list_success(self, host_cluster, test_namespace):
        """正常查询列表"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace
                )
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

    def test_list_with_state_filter(self, host_cluster, test_namespace):
        """按状态过滤 - firing"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace
                )
            )
            api.query_params.state = "firing"
            api.query_params.page = "1"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()

    def test_list_with_state_filter_pending(self, host_cluster, test_namespace):
        """按状态过滤 - pending"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace
                )
            )
            api.query_params.state = "pending"
            api.query_params.page = "1"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()

    def test_list_with_keyword_filter(self, host_cluster, test_namespace):
        """按关键词过滤"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace
                )
            )
            api.query_params.keyword = "test"
            api.query_params.page = "1"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()


# ==================== Member Cluster 多集群测试 ====================

@pytest.mark.alerting_management
@pytest.mark.multi_cluster
class TestListNamespaceAlertsMember:
    """Member 集群 - 查询命名空间告警列表"""

    def test_list_on_member_cluster(self, member_cluster, test_namespace):
        """在 member 集群查询命名空间告警列表"""
        set_current_cluster(member_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(
                    cluster=member_cluster,
                    namespace=test_namespace
                )
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
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(
                    cluster=member_cluster,
                    namespace=test_namespace
                )
            )
            api.query_params.page = "1"
            res = api.send()
            member_items = res.cached_response.raw_response.json().get("items", [])
        finally:
            clear_current_cluster()

        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(
                    cluster=host_cluster,
                    namespace=test_namespace
                )
            )
            api.query_params.page = "1"
            res = api.send()
            host_items = res.cached_response.raw_response.json().get("items", [])
        finally:
            clear_current_cluster()

        logger.info(f"Host 命名空间告警数: {len(host_items)}, Member 命名空间告警数: {len(member_items)}")
