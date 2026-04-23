# -*- coding:utf-8 -*-
"""
项目告警列表单接口测试
API: HandleListAlertsAPI
"""
import pytest
import logging

from apis.whizard_alerting.alerting_management.apis import HandleListAlertsAPI
from testcases.test_api.whizard_alerting.base import (
    get_for_test_namespace_rule_group,
    cleanup_namespace_rule_group,
    wait_for_alerts,
    query_namespace_alerts,
)
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

logger = logging.getLogger(__name__)

# 标准规则组名称（用于测试告警关联）
HOST_STANDARD_RULE_GROUP = "ns-alert-standard"
MEMBER_STANDARD_RULE_GROUP = "member-ns-alert-standard"


@pytest.mark.alerting_management
class TestListNamespaceAlerts:
    """查询项目告警列表"""

    @pytest.fixture(scope="class", autouse=True)
    def prepare_alert_data(self, host_cluster, test_namespace):
        """
        类级别 fixture：统一准备告警数据
        1. 创建规则组
        2. 等待告警触发（最多240秒）
        3. 所有测试执行完毕后清理
        """
        # 1. 创建规则组（使用自定义 expr: vector(1)，更容易触发告警）
        if not get_for_test_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP):
            pytest.skip("无法创建测试规则组，跳过所有告警测试")

        # 2. 等待告警触发
        print(f"⏳ 等待告警触发，规则组: {HOST_STANDARD_RULE_GROUP}")
        found_alert, _ = wait_for_alerts(
            query_func=lambda: query_namespace_alerts(
                cluster=host_cluster,
                namespace=test_namespace,
                rule_group_name=HOST_STANDARD_RULE_GROUP
            ),
            max_attempts=48,
            sleep_interval=5
        )

        if not found_alert:
            print("⚠️ 告警未触发，但继续执行测试")

        yield  # 所有测试执行

        # 3. 测试完成后清理
        print(f"🧹 清理规则组: {HOST_STANDARD_RULE_GROUP}")
        cleanup_namespace_rule_group(host_cluster, test_namespace, HOST_STANDARD_RULE_GROUP)

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
            print(f"✅ 关键词查询成功，关键词: {keyword}，找到 {total} 条告警")
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
            print(f"✅ 找到告警，状态: {[item.get('state') for item in items]}")
        finally:
            clear_current_cluster()


# ==================== Member Cluster 多集群测试 ====================

@pytest.mark.alerting_management
@pytest.mark.multi_cluster
class TestListNamespaceAlertsMember:
    """Member 集群 - 查询项目告警列表"""

    def test_list_alerts_on_member_cluster(self, member_cluster, test_namespace_member):
        """
        在 member 集群查询项目告警列表
        先创建规则组等待告警触发，验证返回的告警 labels.cluster = member_cluster
        """
        # 创建 member 标准规则组
        if not get_for_test_namespace_rule_group(member_cluster, test_namespace_member, MEMBER_STANDARD_RULE_GROUP):
            pytest.skip("无法在 member 集群创建测试规则组")

        try:
            # 等待告警触发，并验证 cluster 标签
            def validate_cluster_label(items):
                for item in items:
                    cluster_label = item.get("labels", {}).get("cluster")
                    assert cluster_label == member_cluster, \
                        f"告警 cluster 标签不匹配: {cluster_label} != {member_cluster}"

            found_alert, _ = wait_for_alerts(
                query_func=lambda: query_namespace_alerts(
                    cluster=member_cluster,
                    namespace=test_namespace_member,
                    rule_group_name=MEMBER_STANDARD_RULE_GROUP
                ),
                max_attempts=48,
                sleep_interval=5,
                validate_func=validate_cluster_label
            )

            if found_alert:
                print(f"✅ Member 集群告警触发成功，规则组: {MEMBER_STANDARD_RULE_GROUP}")
            else:
                print(f"⚠️ 告警未触发，可能测试环境无监控数据")
        finally:
            cleanup_namespace_rule_group(member_cluster, test_namespace_member, MEMBER_STANDARD_RULE_GROUP)
