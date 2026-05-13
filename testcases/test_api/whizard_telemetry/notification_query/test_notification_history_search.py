import pytest

from utils.api_helpers import get_http_info

from testcases.test_api.whizard_telemetry.notification_query.base import (
    search_notifications,
    get_for_test_notification_history,
    make_timestamp,
)


@pytest.mark.notification
class TestNotificationHistoryQuery:
    """通知历史查询"""

    def test_query_success(self):
        """查询通知历史 - 成功"""
        res = search_notifications()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data.get("total"), int)
        assert isinstance(data.get("items"), list)

    def test_query_with_pagination(self):
        """查询通知历史 - 分页"""
        res = search_notifications(from_=0, size=5)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        items = data.get("items") or []
        assert len(items) <= 5

    def test_query_filter_by_alertname(self):
        """查询通知历史 - 按告警名称模糊查询"""
        res = search_notifications(alertname_fuzzy="global-alert")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for item in (data.get("items") or []):
            assert "global-alert" in item.get("alertname", "").lower()

    def test_query_filter_by_severity(self):
        """查询通知历史 - 按告警级别过滤"""
        res = search_notifications(severity="critical")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for item in (data.get("items") or []):
            assert item.get("severity") == "critical"

    def test_query_filter_by_message(self):
        """查询通知历史 - 按消息模糊查询"""
        res = search_notifications(message_fuzzy="summary")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for item in (data.get("items") or []):
            msg = (item.get("message") or "").lower()
            assert "summary" in msg

    def test_query_filter_by_status(self):
        """查询通知历史 - 按状态过滤"""
        res = search_notifications(status="firing")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for item in (data.get("items") or []):
            assert item.get("status") == "firing"

    def test_query_filter_by_namespace(self, test_namespace):
        """查询通知历史 - 按项目模糊查询"""
        res = search_notifications(namespace_fuzzy=test_namespace)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for item in (data.get("items") or []):
            ns = (item.get("namespace") or "").lower()
            assert "host-pro1-test" in ns

    def test_query_filter_by_time_range(self):
        """查询通知历史 - 按时间范围过滤"""
        end_time = make_timestamp(0)
        start_time = make_timestamp(1800)
        res = search_notifications(start_time=start_time, end_time=end_time)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "total" in data


@pytest.mark.notification
@pytest.mark.multi_cluster
class TestNotificationHistoryMemberCluster:
    """Member 集群通知历史查询"""

    def test_member_query(self, member_cluster):
        """Member 集群 - 查询通知历史，验证 cluster 字段"""
        res = search_notifications(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "items" in data
        items = data.get("items") or []
        if items:
            assert items[0].get("cluster") == member_cluster, (
                f"expected cluster={member_cluster}, got {items[0].get('cluster')}"
            )

    def test_member_query_filter_by_alertname(self, member_cluster):
        """Member 集群 - 按告警名称模糊查询"""
        res = search_notifications(cluster=member_cluster, alertname_fuzzy="global-alert")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for item in (data.get("items") or []):
            assert item.get("cluster") == member_cluster