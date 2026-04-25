# -*- coding:utf-8 -*-
"""
全局告警列表单接口测试
API: HandleListGlobalAlertsAPI
"""
import pytest
from loguru import logger

from apis.whizard_alerting.alerting_management.apis import HandleListGlobalAlertsAPI
from testcases.test_api.whizard_alerting.base import is_alert_prewarmed

# 标准规则组名称（用于测试告警关联）
STANDARD_RULE_GROUP = "global-alert-standard"


@pytest.mark.alerting_management
class TestListGlobalAlerts:
    """查询全局告警列表"""

    @pytest.fixture(scope="session", autouse=True)
    def prepare_alert_data(self):
        """
        session 级别 fixture：复用 before_all 预热的告警数据
        不再创建规则组和等待告警，由 after_all 统一清理
        """
        if not is_alert_prewarmed("global", group_name=STANDARD_RULE_GROUP):
            logger.warning(f"告警未预热，规则组: {STANDARD_RULE_GROUP}，测试可能受影响")
        yield

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
        logger.info(f"规则组 {STANDARD_RULE_GROUP} 找到 {total} 条告警")

        rule_groups = [item.get("labels", {}).get("rule_group", "") for item in items]
        assert STANDARD_RULE_GROUP in rule_groups, \
            f"未找到 rule_group 为 {STANDARD_RULE_GROUP} 的告警，实际 rule_groups: {rule_groups}"
