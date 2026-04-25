# -*- coding:utf-8 -*-
"""
项目告警列表单接口测试
API: HandleListAlertsAPI
"""
import pytest
from loguru import logger

from apis.whizard_alerting.alerting_management.apis import HandleListAlertsAPI
from testcases.conftest import host_cluster
from testcases.test_api.whizard_alerting.base import is_alert_prewarmed
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

HOST_STANDARD_RULE_GROUP = "ns-alert-standard"
MEMBER_STANDARD_RULE_GROUP = "member-ns-alert-standard"


@pytest.mark.alerting_management
class TestListNamespaceAlerts:
    """查询项目告警列表"""

    @pytest.fixture(scope="session", autouse=True)
    def prepare_alert_data(self, host_cluster, test_namespace):
        """
        session 级别 fixture：复用 before_all 预热的告警数据
        不再创建规则组和等待告警，由 after_all 统一清理
        """
        if not is_alert_prewarmed("namespace", cluster=host_cluster, namespace=test_namespace, group_name=HOST_STANDARD_RULE_GROUP):
            logger.warning(f"告警未预热，规则组: {HOST_STANDARD_RULE_GROUP}，测试可能受影响")
        yield

    def test_list_success(self, host_cluster, test_namespace):
        """正常查询列表"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                enable_schema_validation=False,
                response=None
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

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
                path_params=HandleListAlertsAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                enable_schema_validation=False,
                response=None
            )
            api.query_params.state = "firing"
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()

    def test_list_with_state_filter_pending(self, host_cluster, test_namespace):
        """按状态过滤 - pending"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                enable_schema_validation=False,
                response=None
            )
            api.query_params.state = "pending"
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()

    def test_list_with_keyword_filter(self, host_cluster, test_namespace, prepare_alert_data):
        """按关键词过滤 - 必须检索到标准资源告警"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                enable_schema_validation=False,
                response=None
            )
            # 使用标准资源的 summary 作为关键词: ns-alert-standard-summary
            keyword = f"{HOST_STANDARD_RULE_GROUP}-summary"
            api.query_params.keyword = keyword
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data

            # 严格校验：必须能检索到内容
            total = data.get("totalItems", 0)
            assert total >= 1, f"关键词 {keyword} 查询失败，未找到告警"
            logger.info(f"关键词查询成功，关键词: {keyword}，找到 {total} 条告警")
        finally:
            clear_current_cluster()

    def test_list_alerts_by_rule_group(self, host_cluster, test_namespace, prepare_alert_data):
        """
        规则组详情查看告警
        使用 fixture 准备的规则组，验证 label_filters 能查询到结果
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(cluster=host_cluster, namespace=test_namespace),
                enable_schema_validation=False,
                response=None
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.ascending = "false"
            api.query_params.sortBy = "activeAt"
            api.query_params.label_filters = f"rule_group={HOST_STANDARD_RULE_GROUP}"
            

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            items = data.get("items") or []

            assert len(items) >= 1, f"未找到规则组 {HOST_STANDARD_RULE_GROUP} 的告警"
            logger.info(f"找到告警，状态: {[item.get('state') for item in items]}")
        finally:
            clear_current_cluster()


@pytest.mark.alerting_management
@pytest.mark.multi_cluster
class TestListNamespaceAlertsMember:
    """Member 集群 - 查询项目告警列表"""

    @pytest.fixture(scope="session", autouse=True)
    def prepare_alert_data(self, member_cluster, test_namespace_member):
        """session 级别，复用 before_all 预热的告警数据"""
        if not is_alert_prewarmed("namespace", cluster=member_cluster, namespace=test_namespace_member, group_name=MEMBER_STANDARD_RULE_GROUP):
            logger.warning(f"Member 集群告警未预热，规则组: {MEMBER_STANDARD_RULE_GROUP}")
        yield

    def test_list_alerts_on_member_cluster(self, member_cluster, test_namespace_member, prepare_alert_data):
        """在 member 集群查询项目告警列表，验证告警来源于正确的集群"""
        set_current_cluster(member_cluster)
        try:
            api = HandleListAlertsAPI(
                path_params=HandleListAlertsAPI.PathParams(cluster=member_cluster, namespace=test_namespace_member)
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"
            api.query_params.label_filters = f"rule_group={MEMBER_STANDARD_RULE_GROUP}"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            items = data.get("items") or []

            if items:
                for item in items:
                    cluster_label = item.get("labels", {}).get("cluster")
                    assert cluster_label == member_cluster, \
                        f"告警 cluster 标签不匹配: {cluster_label} != {member_cluster}"
                logger.info(f"Member 集群告警验证成功，规则组: {MEMBER_STANDARD_RULE_GROUP}")
            else:
                logger.warning(f"未找到 Member 集群告警: {MEMBER_STANDARD_RULE_GROUP}")
        finally:
            clear_current_cluster()
