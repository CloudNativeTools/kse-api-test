import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.log_query.base import (
    query_logs_statistics,
    query_logs_histogram,
    query_logs,
    get_for_test_logs,
    resolve_log_time_range,
)

FILTERS = load_test_data("whizard_telemetry", "log_query/logs", "filters", default={})
PAGINATION = load_test_data("whizard_telemetry", "log_query/logs", "pagination", default={})
HISTOGRAM = load_test_data("whizard_telemetry", "log_query/logs", "histogram", default={})
INVALID_PARAMS = load_test_data("whizard_telemetry", "log_query/logs", "invalid_params", default={})


@pytest.mark.whizard_logs
class TestLogsStatistics:
    """日志统计查询"""

    def test_statistics_success(self):
        """查询日志统计 - 成功"""
        res = query_logs_statistics()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "statistics" in data
        assert "containers" in data["statistics"]
        assert "logs" in data["statistics"]
        assert isinstance(data["statistics"]["containers"], int)
        assert isinstance(data["statistics"]["logs"], int)

    def test_statistics_with_namespace_filter(self):
        """查询日志统计 - 按命名空间过滤"""
        ns_filter = FILTERS.get("namespace_filter", {}).get("namespaces", "default")
        res = query_logs_statistics(namespaces=ns_filter)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_statistics_with_log_query(self):
        """查询日志统计 - 按关键字搜索"""
        log_query = FILTERS.get("log_query", {}).get("log_query", "INFO")
        res = query_logs_statistics(log_query=log_query)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_logs
class TestLogsHistogram:
    """日志直方图查询"""

    def test_histogram_success(self):
        """查询日志直方图 - 成功"""
        res = query_logs_histogram()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "histogram" in data
        assert "total" in data["histogram"]
        assert "histograms" in data["histogram"]
        assert isinstance(data["histogram"]["total"], int)
        assert isinstance(data["histogram"]["histograms"], list)

    def test_histogram_30m_interval(self):
        """查询日志直方图 - 30分钟间隔"""
        interval = HISTOGRAM.get("interval_30m", {}).get("interval", "30m")
        res = query_logs_histogram(interval=interval)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        if data["histogram"]["histograms"]:
            bucket = data["histogram"]["histograms"][0]
            assert "time" in bucket
            assert "count" in bucket

    def test_histogram_1h_interval(self):
        """查询日志直方图 - 1小时间隔"""
        interval = HISTOGRAM.get("interval_1h", {}).get("interval", "1h")
        res = query_logs_histogram(interval=interval)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_histogram_with_namespace_filter(self):
        """查询日志直方图 - 按命名空间过滤"""
        ns_filter = FILTERS.get("namespace_filter", {}).get("namespaces", "default")
        res = query_logs_histogram(namespaces=ns_filter)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_histogram_with_log_query(self):
        """查询日志直方图 - 按关键字搜索"""
        log_query = FILTERS.get("log_query", {}).get("log_query", "INFO")
        res = query_logs_histogram(log_query=log_query)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_logs
class TestLogsQuery:
    """日志列表查询"""

    def test_query_success(self):
        """查询日志列表 - 成功"""
        res = query_logs()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data
        assert "total" in data["query"]
        assert "records" in data["query"]

    def test_query_with_pagination(self):
        """查询日志列表 - 分页"""
        page = PAGINATION.get("page_1", {"from": 0, "size": 5})
        res = query_logs(from_=page["from"], size=page["size"])
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        assert len(records) <= page["size"]

    def test_query_second_page(self):
        """查询日志列表 - 第二页"""
        page = PAGINATION.get("page_2", {"from": 5, "size": 5})
        res = query_logs(from_=page["from"], size=page["size"])
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_namespace(self, test_namespace):
        """查询日志列表 - 按命名空间过滤"""
        res = query_logs(namespaces=test_namespace)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_pod(self):
        """查询日志列表 - 按 Pod 过滤"""
        pods = FILTERS.get("pod_filter", {}).get("pods", "host-nginx")
        res = query_logs(pods=pods)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_container(self):
        """查询日志列表 - 按容器过滤"""
        containers = FILTERS.get("container_filter", {}).get("containers", "nginx")
        res = query_logs(containers=containers)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_log_search(self):
        """查询日志列表 - 按关键字搜索"""
        log_query = FILTERS.get("log_query", {}).get("log_query", "INFO")
        res = query_logs(log_query=log_query)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for record in (data["query"].get("records") or []):
            log_text = record.get("log", "").upper()
            assert log_query.upper() in log_text, (
                f"expected log containing {log_query}, got: {record.get('log')}"
            )

    def test_query_namespace_search(self):
        """查询日志列表 - 按命名空间模糊搜索"""
        ns_search = FILTERS.get("namespace_search", {}).get("namespace_query", "kube")
        res = query_logs(namespace_query=ns_search)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_pod_search(self):
        """查询日志列表 - 按 Pod 模糊搜索"""
        pod_search = FILTERS.get("pod_search", {}).get("pod_query", "nginx")
        res = query_logs(pod_query=pod_search)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_container_search(self):
        """查询日志列表 - 按容器模糊搜索"""
        container_search = FILTERS.get("container_search", {}).get("container_query", "nginx")
        res = query_logs(container_query=container_search)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_logs
class TestLogsEdgeCases:
    """日志查询边界场景"""

    def test_invalid_interval(self):
        """无效的时间间隔 - 应返回错误"""
        invalid = INVALID_PARAMS.get("invalid_interval", {"operation": "histogram", "interval": "invalid"})
        res = query_logs_histogram(interval=invalid["interval"])
        status, text = get_http_info(res)
        assert status == 500, f"expected 500, got {status}"
        assert "search_phase_execution_exception" in text, f"missing expected error type in: {text}"
        assert "Unable to parse interval" in text, f"missing expected error reason in: {text}"

    def test_large_size_param(self):
        """较大的 size 参数"""
        page = PAGINATION.get("page_1", {"from": 0, "size": 5})
        res = query_logs(from_=page["from"], size=100)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

@pytest.mark.whizard_logs
@pytest.mark.multi_cluster
class TestLogsMemberCluster:
    """Member 集群日志查询"""

    def test_member_query(self, member_cluster):
        """Member 集群 - 查询日志列表"""
        res = query_logs(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data

    def test_member_statistics(self, member_cluster, host_cluster):
        """Member 集群 - 日志统计（数据应与 host 集群不同）"""
        host_res = query_logs_statistics(cluster=host_cluster)
        host_data = host_res.cached_response.raw_response.json().get("statistics", {})

        member_res = query_logs_statistics(cluster=member_cluster)
        status, text = get_http_info(member_res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = member_res.cached_response.raw_response.json()
        assert "statistics" in data

        assert data["statistics"] != host_data, (
            f"member statistics matches host, expected different data. host: {host_data}, member: {data['statistics']}"
        )

    def test_member_histogram(self, member_cluster, host_cluster):
        """Member 集群 - 日志直方图（数据应与 host 集群不同）"""
        host_res = query_logs_histogram(cluster=host_cluster)
        host_data = host_res.cached_response.raw_response.json().get("histogram", {})

        member_res = query_logs_histogram(cluster=member_cluster)
        status, text = get_http_info(member_res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = member_res.cached_response.raw_response.json()
        assert "histogram" in data

        assert data["histogram"] != host_data, (
            f"member histogram matches host, expected different data. host: {host_data}, member: {data['histogram']}"
        )