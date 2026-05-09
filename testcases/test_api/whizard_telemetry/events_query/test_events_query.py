import pytest

from apis.whizard_telemetry.events_query.apis import QueryEventsAPI
from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.events_query.base import (
    query_events_statistics,
    query_events_histogram,
    query_events,
    get_for_test_events,
    resolve_event_time_range,
)

FILTERS = load_test_data("whizard_telemetry", "events_query/events", "filters", default={})
PAGINATION = load_test_data("whizard_telemetry", "events_query/events", "pagination", default={})
HISTOGRAM = load_test_data("whizard_telemetry", "events_query/events", "histogram", default={})
INVALID_PARAMS = load_test_data("whizard_telemetry", "events_query/events", "invalid_params", default={})


@pytest.mark.whizard_events
class TestEventsStatistics:
    """事件统计查询"""

    def test_statistics_success(self):
        """查询事件统计 - 成功"""
        res = query_events_statistics()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "statistics" in data
        assert "resources" in data["statistics"]
        assert "events" in data["statistics"]
        assert isinstance(data["statistics"]["resources"], int)
        assert isinstance(data["statistics"]["events"], int)


@pytest.mark.whizard_events
class TestEventsHistogram:
    """事件直方图查询"""

    def test_histogram_success(self):
        """查询事件直方图 - 成功"""
        res = query_events_histogram()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "histogram" in data
        assert "total" in data["histogram"]
        assert "buckets" in data["histogram"]
        assert isinstance(data["histogram"]["total"], int)
        assert isinstance(data["histogram"]["buckets"], list)

    def test_histogram_30m_interval(self):
        """查询事件直方图 - 30分钟间隔"""
        interval = HISTOGRAM.get("interval_30m", {}).get("interval", "30m")
        res = query_events_histogram(interval=interval)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        if data["histogram"]["buckets"]:
            bucket = data["histogram"]["buckets"][0]
            assert "time" in bucket
            assert "count" in bucket

    def test_histogram_1h_interval(self):
        """查询事件直方图 - 1小时间隔"""
        interval = HISTOGRAM.get("interval_1h", {}).get("interval", "1h")
        res = query_events_histogram(interval=interval)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_histogram_with_type_filter(self):
        """查询事件直方图 - 按类型过滤"""
        type_filter = FILTERS.get("type_normal", {}).get("type_filter", "Normal")
        res = query_events_histogram(type_filter=type_filter)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_histogram_with_kind_filter(self):
        """查询事件直方图 - 按资源类型过滤"""
        kind_filter = FILTERS.get("kind_pod", {}).get("involved_object_kind_filter", "Pod")
        res = query_events_histogram(involved_object_kind_filter=kind_filter)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_events
class TestEventsQuery:
    """事件列表查询"""

    def test_query_success(self):
        """查询事件列表 - 成功"""
        res = query_events()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data
        assert "total" in data["query"]
        assert "records" in data["query"]

    def test_query_with_pagination(self):
        """查询事件列表 - 分页"""
        page = PAGINATION.get("page_1", {"from": 0, "size": 5})
        res = query_events(from_=page["from"], size=page["size"])
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records", [])
        assert len(records) <= page["size"]

    def test_query_second_page(self):
        """查询事件列表 - 第二页"""
        page = PAGINATION.get("page_2", {"from": 5, "size": 5})
        res = query_events(from_=page["from"], size=page["size"])
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_type_warning(self):
        """查询事件列表 - 过滤 Warning 类型"""
        filter_params = FILTERS.get("type_warning", {"type_filter": "Warning"})
        res = query_events(**filter_params)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for record in (data["query"].get("records") or []):
            assert record.get("type") == filter_params["type_filter"]

    def test_query_filter_by_type_normal(self):
        """查询事件列表 - 过滤 Normal 类型"""
        filter_params = FILTERS.get("type_normal", {"type_filter": "Normal"})
        res = query_events(**filter_params)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for record in (data["query"].get("records") or []):
            assert record.get("type") == filter_params["type_filter"]

    def test_query_filter_by_namespace(self, test_namespace):
        """查询事件列表 - 按命名空间过滤"""
        res = query_events(involved_object_namespace_filter=test_namespace)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_kind_pod(self):
        """查询事件列表 - 按资源类型过滤 (Pod)"""
        kind_filter = FILTERS.get("kind_pod", {}).get("involved_object_kind_filter", "Pod")
        res = query_events(involved_object_kind_filter=kind_filter)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_reason(self):
        """查询事件列表 - 按原因过滤"""
        res = query_events(reason_filter="Started")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_message_search(self):
        """查询事件列表 - 按消息搜索"""
        msg_search = FILTERS.get("message_search", {}).get("message_search", "Started")
        res = query_events(message_search=msg_search)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_namespace_search(self):
        """查询事件列表 - 按命名空间模糊搜索"""
        ns_search = FILTERS.get("namespace_search", {}).get("involved_object_namespace_search", "kube")
        res = query_events(involved_object_namespace_search=ns_search)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_workspace(self, test_workspace):
        """查询事件列表 - 按企业空间过滤"""
        res = query_events(workspace_filter=test_workspace)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data

    def test_query_filter_by_resource_name(self):
        """查询事件列表 - 按资源名称过滤"""
        res = query_events(involved_object_name_filter="host-nginx")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data


@pytest.mark.whizard_events
class TestEventsEdgeCases:
    """Events 查询边界场景"""

    def test_invalid_interval(self):
        """无效的时间间隔 - 应返回错误"""
        invalid = INVALID_PARAMS.get("invalid_interval", {"operation": "histogram", "interval": "invalid"})
        res = query_events_histogram(interval=invalid["interval"])
        status, text = get_http_info(res)
        assert status == 500, f"expected == 500, got {status}"
        assert "search_phase_execution_exception" in text, f"missing expected error type in: {text}"
        assert "Unable to parse interval" in text, f"missing expected error reason in: {text}"

    def test_large_size_param(self):
        """较大的 size 参数"""
        page = PAGINATION.get("page_1", {"from": 0, "size": 5})
        res = query_events(from_=page["from"], size=100)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_events
@pytest.mark.multi_cluster
class TestEventsMemberCluster:
    """Member 集群 Events 查询"""

    def test_member_query(self, member_cluster):
        """Member 集群 - 查询事件列表"""
        res = query_events(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data
        records = data["query"].get("records", [])
        if records:
            assert records[0].get("cluster") == member_cluster, (
                f"expected cluster={member_cluster}, got {records[0].get('cluster')}"
            )

    def test_member_statistics(self, member_cluster, host_cluster):
        """Member 集群 - 事件统计（数据应与 host 集群不同）"""
        host_res = query_events_statistics(cluster=host_cluster)
        host_data = host_res.cached_response.raw_response.json().get("statistics", {})

        member_res = query_events_statistics(cluster=member_cluster)
        status, text = get_http_info(member_res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = member_res.cached_response.raw_response.json()
        assert "statistics" in data

        assert data["statistics"] != host_data, (
            f"member statistics matches host, expected different data. host: {host_data}, member: {data['statistics']}"
        )

    def test_member_histogram(self, member_cluster, host_cluster):
        """Member 集群 - 事件直方图（数据应与 host 集群不同）"""
        host_res = query_events_histogram(cluster=host_cluster)
        host_data = host_res.cached_response.raw_response.json().get("histogram", {})

        member_res = query_events_histogram(cluster=member_cluster)
        status, text = get_http_info(member_res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = member_res.cached_response.raw_response.json()
        assert "histogram" in data

        assert data["histogram"] != host_data, (
            f"member histogram matches host, expected different data. host: {host_data}, member: {data['histogram']}"
        )