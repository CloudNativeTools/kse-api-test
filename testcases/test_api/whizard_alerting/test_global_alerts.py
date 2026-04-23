# -*- coding:utf-8 -*-
"""
全局告警列表单接口测试
API: HandleListGlobalAlertsAPI

测试策略：
1. 全局告警是Global级别，不区分多集群
2. 告警需要等待触发，使用fixture准备规则组数据
3. 验证告警状态（pending/firing）
4. 支持规则组过滤查询
"""
import pytest
import logging

from apis.whizard_alerting.alerting_management.apis import HandleListGlobalAlertsAPI
from testcases.test_api.whizard_alerting.base import (
    get_for_test_global_rule_group,
    cleanup_global_rule_group,
    wait_for_alerts,
    query_global_alerts,
)

logger = logging.getLogger(__name__)

# 标准规则组名称（用于测试告警关联）
STANDARD_RULE_GROUP = "global-alert-standard"


@pytest.mark.alerting_management
class TestListGlobalAlerts:
    """查询全局告警列表"""

    @pytest.fixture(scope="class", autouse=True)
    def prepare_alert_data(self):
        """
        类级别 fixture：统一准备告警数据
        1. 创建规则组（使用自定义 expr: vector(1)，更容易触发告警）
        2. 等待告警触发（最多240秒）
        3. 所有测试执行完毕后清理
        """
        # 1. 创建规则组
        if not get_for_test_global_rule_group(STANDARD_RULE_GROUP):
            pytest.skip("无法创建测试规则组，跳过所有告警测试")

        # 2. 等待告警触发
        logger.info(f"⏳ 等待告警触发，规则组: {STANDARD_RULE_GROUP}")
        found_alert, _ = wait_for_alerts(
            query_func=lambda: query_global_alerts(
                rule_group_name=STANDARD_RULE_GROUP
            ),
            max_attempts=48,
            sleep_interval=5
        )

        if not found_alert:
            logger.warning("⚠️ 告警未触发，但继续执行测试")

        yield

        # 3. 测试完成后清理
        logger.info(f"🧹 清理规则组: {STANDARD_RULE_GROUP}")
        cleanup_global_rule_group(STANDARD_RULE_GROUP)

    def test_list_all_success(self):
        """正常查询列表"""
        api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.sortBy = "activeAt"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

        total = data.get("totalItems", 0)
        assert total >= 1, f"关键词查询结果应 >=1，实际: {total}"

    def test_list_with_state_filter_firing(self):
        """按状态过滤 - firing"""
        api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.state = "firing"
        api.query_params.page = "1"
        api.query_params.limit = "10"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

    def test_list_with_state_filter_pending(self):
        """按状态过滤 - pending"""
        api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.state = "pending"
        api.query_params.page = "1"
        api.query_params.limit = "10"
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

    def test_list_with_keyword_filter(self, prepare_alert_data):
        """按关键词过滤 - 必须检索到标准资源告警"""
        keyword = f"{STANDARD_RULE_GROUP}-summary"
        api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.keyword = keyword
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data

        total = data.get("totalItems", 0)
        assert total >= 1, f"关键词查询结果应 >=1，实际: {total}"

        items = data.get("items") or []
        alertnames = [item.get("labels", {}).get("alertname", "") for item in items]
        assert f"{STANDARD_RULE_GROUP}-alert" in alertnames, \
            f"未找到 alertname 为 {STANDARD_RULE_GROUP}-alert 的告警，实际 alertnames: {alertnames}"

    def test_list_custom_alerts(self):
        """查询自定义告警列表 (builtin=false)"""
        api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.builtin = "false"
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.sortBy = "activeAt"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

    def test_list_builtin_alerts(self):
        """查询内置告警列表 (builtin=true)"""
        api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.builtin = "true"
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.sortBy = "activeAt"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

        total = data.get("totalItems", 0)
        assert total >= 1, f"内置告警数量应 >=1，实际: {total}"

    def test_list_alerts_by_rule_group(self, prepare_alert_data):
        """
        规则组详情查看告警
        使用 fixture 准备的规则组，验证 label_filters 能查询到结果
        """
        api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.ascending = "false"
        api.query_params.sortBy = "activeAt"
        api.query_params.label_filters = f"rule_group={STANDARD_RULE_GROUP}"
        api.query_params.builtin = "false"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        items = data.get("items") or []

        total = data.get("totalItems", 0)
        assert total > 0, f"规则组 {STANDARD_RULE_GROUP} 查询结果应 >0，实际: {total}"
        print(f"规则组 {STANDARD_RULE_GROUP} 找到 {total} 条告警")

        rule_groups = [item.get("labels", {}).get("rule_group", "") for item in items]
        assert STANDARD_RULE_GROUP in rule_groups, \
            f"未找到 rule_group 为 {STANDARD_RULE_GROUP} 的告警，实际 rule_groups: {rule_groups}"
