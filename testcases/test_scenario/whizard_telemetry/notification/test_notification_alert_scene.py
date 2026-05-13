"""
告警通知链路场景测试
流程：创建临时规则组 -> 等待告警触发 -> 轮询通知历史 -> 验证告警通知可查 -> 清理临时规则组
"""
import time
import pytest
import logging

from apis.whizard_alerting.alerting_management.apis import (
    HandleCreateGlobalRuleGroupAPI,
    HandleListGlobalAlertsAPI,
)
from apis.whizard_telemetry.notification_query.apis import (
    SearchNotificationAPI,
)
from testcases.test_api.whizard_telemetry.notification.base import (
    get_for_test_email_config,
    get_for_test_email_receiver,
)
from testcases.test_api.whizard_alerting.base import (
    cleanup_global_rule_group,
    wait_for_alerts,
)
from utils.test_data_helper import load_test_data

logger = logging.getLogger(__name__)

TEMP_GROUP_PREFIX = "notification-verify"


@pytest.mark.notification_scene
class TestNotificationAlertScene:
    """告警通知链路场景测试"""

    @pytest.fixture(scope="class", autouse=True)
    def prepare_data(self):
        """创建临时规则组并等待告警触发，测试结束后清理"""
        if not get_for_test_email_config():
            pytest.skip("无法准备 email 通知配置，跳过场景")
        if not get_for_test_email_receiver():
            pytest.skip("无法准备 email 接收者，跳过场景")

        group_name = f"{TEMP_GROUP_PREFIX}-{int(time.time())}"
        alert_name = f"{group_name}-alert"

        request_body = load_test_data(
            "whizard_alerting", "alerting_management/global_rule_groups", "global_rule_group_custom"
        )
        request_body["metadata"]["name"] = group_name
        request_body["spec"]["rules"][0]["alert"] = alert_name
        request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{group_name}-summary"
        request_body["spec"]["rules"][0]["annotations"]["message"] = f"{group_name}-message"

        create_api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = create_api.send()
        if res.cached_response.raw_response.status_code not in (200, 201):
            pytest.skip(f"无法创建临时规则组: {group_name}")

        logger.info(f"临时规则组创建成功: {group_name}")

        logger.info(f"等待告警触发: {alert_name}")
        def query_global_alerts():
            api = HandleListGlobalAlertsAPI(
                enable_schema_validation=False,
                response=None
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.builtin = "false"
            api.query_params.label_filters = f"rule_group={group_name}"
            res = api.send()
            if res.cached_response.raw_response.status_code == 200:
                return res.cached_response.raw_response.json().get("items") or []
            return None

        found_alert, _ = wait_for_alerts(query_global_alerts, max_attempts=48, sleep_interval=5)
        if not found_alert:
            cleanup_global_rule_group(group_name)
            pytest.skip(f"告警未触发: {alert_name}")

        logger.info(f"告警已触发: {alert_name}")

        TestNotificationAlertScene.alert_name = alert_name
        TestNotificationAlertScene.group_name = group_name

        yield

        logger.info(f"清理临时规则组: {group_name}")
        cleanup_global_rule_group(group_name)

    def test_01_query_notification_history(self):
        """查询通知历史，验证 API 响应正确"""
        api = SearchNotificationAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.cluster = "host"
        api.query_params.size = 10
        api.query_params.from_ = 0

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "total" in data

        total = data.get("total", 0)
        items = data.get("items") or []
        logger.info(f"通知历史查询成功，total={total}, 返回条数={len(items)}")

    def test_02_verify_alert_in_notification_history(self):
        """轮询通知历史，验证临时规则组的告警通知已到达"""
        alert_name = self.alert_name
        logger.info(f"等待告警通知出现: {alert_name}")

        max_retries = 12
        retry_interval = 15
        last_names = []

        for attempt in range(1, max_retries + 1):
            logger.info(f"轮询第 {attempt}/{max_retries} 次...")

            api = SearchNotificationAPI(
                enable_schema_validation=False,
                response=None
            )
            api.query_params.cluster = "host"
            api.query_params.size = 10
            api.query_params.from_ = 0
            api.query_params.alertname_fuzzy = alert_name

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            items = data.get("items") or []
            total = data.get("total", 0)
            last_names = [item.get("alertname", "") for item in items]

            if total > 0:
                logger.info(f"✓ 告警通知已出现 (第 {attempt} 次轮询, 共 {total} 条)")
                logger.info(f"  通知名称: {last_names}")
                return

            if attempt < max_retries:
                logger.info(f"通知尚未出现，{retry_interval}s 后重试...")
                time.sleep(retry_interval)

        pytest.fail(
            f"轮询 {max_retries * retry_interval}s 后通知历史中仍未找到告警通知。"
            f"告警名: {alert_name}, 最新通知历史: {last_names[:10]}"
        )