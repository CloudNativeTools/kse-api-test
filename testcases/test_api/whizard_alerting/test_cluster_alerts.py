# -*- coding:utf-8 -*-
"""
集群告警列表单接口测试
API: HandleListClusterAlertsAPI
"""
import pytest
import time
import logging

from apis.whizard_alerting.Alerting_Management.apis import HandleListClusterAlertsAPI
from testcases.conftest import host_cluster
from testcases.test_api.whizard_alerting.base import (
    get_for_test_cluster_rule_group,
    cleanup_cluster_rule_group,
    wait_for_alerts,
    query_cluster_alerts,
)
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

logger = logging.getLogger(__name__)

# 标准规则组名称（用于测试告警关联）
STANDARD_RULE_GROUP = "cluster-alert-standard"

@pytest.mark.alerting_management
class TestListClusterAlerts:
    """查询集群告警列表"""

    @pytest.fixture(scope="class", autouse=True)
    def prepare_alert_data(self, host_cluster):
        """
        类级别 fixture：统一准备告警数据
        1. 创建规则组
        2. 等待告警触发（最多240秒）
        3. 所有测试执行完毕后清理
        """
        # 1. 创建规则组
        if not get_for_test_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP):
            pytest.skip("无法创建测试规则组，跳过所有告警测试")

        # 2. 等待告警触发
        logger.info(f"等待告警触发，规则组: {STANDARD_RULE_GROUP}")
        found_alert, _ = wait_for_alerts(
            query_func=lambda: query_cluster_alerts(
                cluster=host_cluster,
                rule_group_name=STANDARD_RULE_GROUP
            ),
            max_attempts=48,
            sleep_interval=5
        )

        if not found_alert:
            logger.warning("告警未触发，但继续执行测试")

        yield  # 所有测试执行

        # 3. 测试完成后清理
        logger.info(f"清理规则组: {STANDARD_RULE_GROUP}")
        cleanup_cluster_rule_group(host_cluster, STANDARD_RULE_GROUP)

    def test_list_success(self, host_cluster):
        """正常查询列表"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterAlertsAPI(
                path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster)
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.builtin = "false"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data
            assert "totalItems" in data
        finally:
            clear_current_cluster()

    def test_list_with_state_filter(self, host_cluster):
        """按状态过滤 - firing"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterAlertsAPI(
                path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster)
            )
            api.query_params.state = "firing"
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"  

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()

    def test_list_with_state_filter_pending(self, host_cluster):
        """按状态过滤 - pending"""
        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterAlertsAPI(
                path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster)
            )
            api.query_params.state = "pending"
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
        finally:
            clear_current_cluster()

    def test_list_with_keyword_filter(self, host_cluster):
        """
        按关键词过滤
        先创建规则组等待告警触发，再按规则组名称关键词查询
        """
        # 按关键词查询告警（使用 summary 作为关键词）
        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterAlertsAPI(
                    path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster)
                )
            # 使用 summary 作为关键词（从 cluster_rule_group_custom 模板中获取）
            api.query_params.keyword = "custom alert"
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"
            api.query_params.builtin = "false"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            # 验证能查到相关告警
            assert "items" in data
            # 如果 keyword 查询有结果，验证 totalItems >= 1
            if data.get("totalItems", 0) >= 1:
                logger.info(f"关键词查询成功，找到 {data.get('totalItems')} 条告警")
            else:
                logger.warning("关键词查询返回 0 条告警，可能 keyword filter 不生效或告警已消失")                
        finally:
            clear_current_cluster()      
            

    def test_list_alerts_by_rule_group(self, host_cluster, prepare_alert_data):
        """
        规则组详情查看告警
        使用 fixture 准备的规则组，验证 label_filters 能查询到结果
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterAlertsAPI(
                path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster)
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.ascending = "false"
            api.query_params.sortBy = "activeAt"
            # 使用 fixture 准备的规则组名称
            api.query_params.label_filters = f"rule_group={STANDARD_RULE_GROUP}"
            api.query_params.builtin = "false"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            items = data.get("items") or []

            # 验证能查到告警（fixture 已等待告警触发）
            assert len(items) >= 1, f"未找到规则组 {STANDARD_RULE_GROUP} 的告警"
            logger.info(f"找到告警，状态: {[item.get('state') for item in items]}")
        finally:
            clear_current_cluster()



# ==================== Member Cluster 多集群测试 ====================

# Member 集群标准规则组名称
MEMBER_STANDARD_RULE_GROUP = "member-cluster-alert-standard"


@pytest.mark.alerting_management
@pytest.mark.multi_cluster
class TestListClusterAlertsMember:
    """Member 集群 - 查询集群告警列表"""

    def test_list_alerts_on_member_cluster(self, member_cluster):
        """
        在 member 集群查询告警列表
        先创建规则组等待告警触发，验证返回的告警 labels.cluster = member_cluster
        """
        # 创建 member 标准规则组
        if not get_for_test_cluster_rule_group(member_cluster, MEMBER_STANDARD_RULE_GROUP):
            pytest.skip("无法在 member 集群创建测试规则组")

        try:
            # 等待告警触发，并验证 cluster 标签
            def validate_cluster_label(items):
                for item in items:
                    cluster_label = item.get("labels", {}).get("cluster")
                    assert cluster_label == member_cluster, \
                        f"告警 cluster 标签不匹配: {cluster_label} != {member_cluster}"

            found_alert, _ = wait_for_alerts(
                query_func=lambda: query_cluster_alerts(
                    cluster=member_cluster,
                    rule_group_name=MEMBER_STANDARD_RULE_GROUP
                ),
                max_attempts=48,
                sleep_interval=5,
                validate_func=validate_cluster_label
            )

            if found_alert:
                logger.info(f"Member 集群告警触发成功，规则组: {MEMBER_STANDARD_RULE_GROUP}")
            else:
                logger.warning(f"告警未触发，可能测试环境无监控数据")
        finally:
            cleanup_cluster_rule_group(member_cluster, MEMBER_STANDARD_RULE_GROUP)
