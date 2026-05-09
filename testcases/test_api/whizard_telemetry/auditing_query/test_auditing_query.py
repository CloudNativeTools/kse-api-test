from loguru import logger
import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.auditing_query.base import (
    query_auditing_statistics,
    query_auditing_histogram,
    query_auditing,
)

FILTERS = load_test_data("whizard_telemetry", "auditing_query/auditing", "filters", default={})
PAGINATION = load_test_data("whizard_telemetry", "auditing_query/auditing", "pagination", default={})
HISTOGRAM = load_test_data("whizard_telemetry", "auditing_query/auditing", "histogram", default={})
INVALID_PARAMS = load_test_data("whizard_telemetry", "auditing_query/auditing", "invalid_params", default={})


@pytest.mark.whizard_auditing
class TestAuditingStatistics:
    """审计统计查询"""

    def test_statistics_success(self):
        """查询审计统计 - 成功"""
        res = query_auditing_statistics()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "statistics" in data
        assert "events" in data["statistics"]
        assert "resources" in data["statistics"]
        assert isinstance(data["statistics"]["events"], int)
        assert isinstance(data["statistics"]["resources"], int)

@pytest.mark.whizard_auditing
class TestAuditingHistogram:
    """审计直方图查询"""

    def test_histogram_success(self):
        """查询审计直方图 - 成功"""
        res = query_auditing_histogram()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "histogram" in data
        assert "total" in data["histogram"]
        assert "buckets" in data["histogram"]
        assert isinstance(data["histogram"]["total"], int)
        assert isinstance(data["histogram"]["buckets"], list)

    def test_histogram_30m_interval(self):
        """查询审计直方图 - 30分钟间隔"""
        interval = HISTOGRAM.get("interval_30m", {}).get("interval", "30m")
        res = query_auditing_histogram(interval=interval)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        if data["histogram"]["buckets"]:
            bucket = data["histogram"]["buckets"][0]
            assert "time" in bucket
            assert "count" in bucket

    def test_histogram_1h_interval(self):
        """查询审计直方图 - 1小时间隔"""
        interval = HISTOGRAM.get("interval_1h", {}).get("interval", "1h")
        res = query_auditing_histogram(interval=interval)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_histogram_with_verb_filter(self):
        """查询审计直方图 - 按操作行为过滤"""
        verb = FILTERS.get("verb_post", {}).get("verb_filter", "POST")
        res = query_auditing_histogram(verb_filter=verb)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_auditing
class TestAuditingQuery:
    """审计列表查询"""

    def test_query_success(self):
        """查询审计列表 - 成功"""
        res = query_auditing()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data
        assert "total" in data["query"]
        assert "records" in data["query"]

    def test_query_with_pagination(self):
        """查询审计列表 - 分页"""
        page = PAGINATION.get("page_1", {"from": 0, "size": 5})
        res = query_auditing(from_=page["from"], size=page["size"])
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records", [])
        assert len(records) <= page["size"]

    def test_query_second_page(self):
        """查询审计列表 - 第二页"""
        page = PAGINATION.get("page_2", {"from": 5, "size": 5})
        res = query_auditing(from_=page["from"], size=page["size"])
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_verb_create(self):
        """查询审计列表 - 过滤 create 操作"""
        verb = FILTERS.get("verb_create", {}).get("verb_filter", "create")
        res = query_auditing(verb_filter=verb)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for record in (data["query"].get("records") or []):
            assert record.get("Verb") == verb, (
                f"expected verb={verb}, got {record.get('Verb')}"
            )

    def test_query_filter_by_namespace(self, test_namespace):
        """查询审计列表 - 按命名空间过滤"""
        res = query_auditing(objectref_namespace_filter=test_namespace)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_resource(self):
        """查询审计列表 - 按资源类型过滤"""
        resource = FILTERS.get("resource_deployment", {}).get("objectref_resource_filter", "deployments")
        res = query_auditing(objectref_resource_filter=resource)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_filter_by_response_code(self):
        """查询审计列表 - 按响应码过滤"""
        code = FILTERS.get("response_code_200", {}).get("response_code_filter", "200")
        res = query_auditing(response_code_filter=code)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_user_search(self):
        """查询审计列表 - 按用户模糊搜索"""
        user = FILTERS.get("user_search", {}).get("user_search", "admin")
        res = query_auditing(user_search=user)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_query_source_ip_search(self):
        """查询审计列表 - 按源 IP 搜索"""
        ip = FILTERS.get("source_ip_search", {}).get("source_ip_search", "10.")
        res = query_auditing(source_ip_search=ip)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        for record in (data["query"].get("records") or []):
            source_ips = record.get("SourceIPs", "")
            if isinstance(source_ips, list):
                source_ips = source_ips[0] if source_ips else ""
            assert ip in source_ips, (
                f"expected SourceIPs containing {ip}, got {record.get('SourceIPs')}"
            )

    def test_query_filter_by_resource_name(self):
        """查询审计列表 - 按资源名称过滤"""
        res = query_auditing(objectref_name_filter="host-nginx")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data
        for record in (data["query"].get("records") or []):
            assert "host-nginx" in record.get("ObjectRef", {}).get("Name", ""), (
                f"expected ObjectRef.Name containing host-nginx, got {record.get('ObjectRef', {})}"
            )

    def test_query_filter_by_workspace(self, test_workspace):
        """查询审计列表 - 按企业空间过滤"""
        res = query_auditing(workspace_filter=test_workspace)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data


@pytest.mark.whizard_auditing
class TestAuditingEdgeCases:
    """审计查询边界场景"""

    def test_invalid_interval(self):
        """无效的时间间隔 - 应返回错误"""
        invalid = INVALID_PARAMS.get("invalid_interval", {"operation": "histogram", "interval": "invalid"})
        res = query_auditing_histogram(interval=invalid["interval"])
        status, text = get_http_info(res)
        assert status == 500, f"expected == 500, got {status}"
        assert "search_phase_execution_exception" in text, f"missing expected error type in: {text}"
        assert "Unable to parse interval" in text, f"missing expected error reason in: {text}"

    def test_large_size_param(self):
        """较大的 size 参数"""
        page = PAGINATION.get("page_1", {"from": 0, "size": 5})
        res = query_auditing(from_=page["from"], size=100)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_auditing
@pytest.mark.multi_cluster
class TestAuditingMemberCluster:
    """Member 集群审计查询"""

    def test_member_query(self, member_cluster):
        """Member 集群 - 查询审计列表"""
        res = query_auditing(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data
        records = data["query"].get("records", [])
        if records:
            assert records[0].get("Cluster") == member_cluster, (
                f"expected Cluster={member_cluster}, got {records[0].get('Cluster')}"
            )

    def test_member_statistics(self, member_cluster, host_cluster):
        """Member 集群 - 审计统计（数据应与 host 集群不同）"""
        host_res = query_auditing_statistics(cluster=host_cluster)
        host_data = host_res.cached_response.raw_response.json().get("statistics", {})

        member_res = query_auditing_statistics(cluster=member_cluster)
        status, text = get_http_info(member_res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = member_res.cached_response.raw_response.json()
        assert "statistics" in data

        assert data["statistics"] != host_data, (
            f"member statistics matches host, expected different data. host: {host_data}, member: {data['statistics']}"
        )

    def test_member_histogram(self, member_cluster, host_cluster):
        """Member 集群 - 审计直方图（数据应与 host 集群不同）"""
        host_res = query_auditing_histogram(cluster=host_cluster)
        host_data = host_res.cached_response.raw_response.json().get("histogram", {})

        member_res = query_auditing_histogram(cluster=member_cluster)
        status, text = get_http_info(member_res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = member_res.cached_response.raw_response.json()
        assert "histogram" in data

        assert data["histogram"] != host_data, (
            f"member histogram matches host, expected different data. host: {host_data}, member: {data['histogram']}"
        )