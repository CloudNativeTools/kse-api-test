import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.auditing_query.base import (
    query_auditing,
    query_auditing_statistics,
    query_auditing_histogram,
    get_for_test_auditing,
)

FILTERS = load_test_data("whizard_telemetry", "auditing_query/auditing", "filters", default={})
PAGINATION = load_test_data("whizard_telemetry", "auditing_query/auditing", "pagination", default={})


@pytest.mark.whizard_auditing_scene
class TestAuditingAnalysisWorkflow:
    """
    审计分析工作流场景测试
    1. 获取统计概览 -> 2. 获取直方图趋势 -> 3. 查询最近审计列表
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_auditing():
            pytest.skip("审计查询环境不可用")

    def test_01_get_statistics_overview(self):
        """步骤1: 获取审计统计概览"""
        res = query_auditing_statistics()
        status, text = get_http_info(res)
        assert status == 200, f"查询审计统计失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "statistics" in data, "响应中缺少 statistics 字段"
        self.stat_events = data["statistics"].get("events", 0)
        self.stat_resources = data["statistics"].get("resources", 0)
        assert isinstance(self.stat_events, int)
        assert isinstance(self.stat_resources, int)

    def test_02_get_histogram_trend(self):
        """步骤2: 获取审计直方图趋势"""
        res = query_auditing_histogram()
        status, text = get_http_info(res)
        assert status == 200, f"查询审计直方图失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "histogram" in data, "响应中缺少 histogram 字段"
        histogram = data["histogram"]
        assert "total" in histogram
        assert "buckets" in histogram
        assert isinstance(histogram["total"], int)
        assert isinstance(histogram["buckets"], list)

    def test_03_query_recent_auditing(self):
        """步骤3: 查询最近审计列表"""
        res = query_auditing()
        status, text = get_http_info(res)
        assert status == 200, f"查询审计列表失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data, "响应中缺少 query 字段"
        self.total_records = data["query"].get("total", 0)
        self.records = data["query"].get("records", [])
        assert isinstance(self.total_records, int)

    def test_04_filter_by_verb(self):
        """步骤4: 按操作行为过滤查询"""
        verb = FILTERS.get("verb_create", {}).get("verb_filter", "create")
        res = query_auditing(verb_filter=verb)
        status, text = get_http_info(res)
        assert status == 200, f"按操作行为过滤查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        for record in records:
            assert record.get("Verb") == verb, \
                f"期望 Verb={verb}，实际: {record.get('Verb')}"

    def test_05_filter_by_namespace(self, test_namespace):
        """步骤5: 按命名空间过滤查询"""
        res = query_auditing(
            objectref_namespace_filter=test_namespace,
        )
        status, text = get_http_info(res)
        assert status == 200, f"按命名空间过滤查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        for record in records:
            ns = record.get("objectRef", {}).get("namespace", "")
            assert ns == test_namespace, \
                f"期望 namespace={test_namespace}，实际: {ns}"

    def test_06_filter_by_resource_and_verify(self, test_namespace):
        """步骤6: 组合资源类型和命名空间过滤"""
        resource = FILTERS.get("resource_deployment", {}).get("objectref_resource_filter", "deployments")
        res = query_auditing(
            objectref_namespace_filter=test_namespace,
            objectref_resource_filter=resource,
        )
        status, text = get_http_info(res)
        assert status == 200, f"组合过滤查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        for record in records:
            obj = record.get("objectRef", {})
            assert obj.get("namespace") == test_namespace
            assert obj.get("resource") == resource

    def test_07_pagination_across_pages(self):
        """步骤7: 分页查询验证"""
        page_1 = PAGINATION.get("page_1", {"from": 0, "size": 5})
        page_2 = PAGINATION.get("page_2", {"from": 5, "size": 5})
        res_page1 = query_auditing(time_range_key="last_3h", from_=page_1["from"], size=page_1["size"])
        status1, _ = get_http_info(res_page1)
        assert status1 == 200
        data1 = res_page1.cached_response.raw_response.json()

        res_page2 = query_auditing(time_range_key="last_3h", from_=page_2["from"], size=page_2["size"])
        status2, _ = get_http_info(res_page2)
        assert status2 == 200
        data2 = res_page2.cached_response.raw_response.json()

        records1 = data1["query"].get("records") or []
        records2 = data2["query"].get("records") or []

        total = data1["query"].get("total", 0)
        if records1 and records2 and total > 5:
            assert records1 != records2, "两页数据完全相同，分页可能未生效"


@pytest.mark.whizard_auditing_scene
@pytest.mark.multi_cluster
class TestAuditingMultiClusterComparison:
    """
    多集群审计对比场景测试

    验证 Member 集群的审计查询均正常
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_auditing():
            pytest.skip("审计查询环境不可用")

    def test_01_member_statistics(self, member_cluster):
        """Member 集群 - 审计统计"""
        res = query_auditing_statistics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群统计查询失败: {status}, {text}"

    def test_02_member_histogram(self, member_cluster):
        """Member 集群 - 审计直方图"""
        res = query_auditing_histogram(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群直方图查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "histogram" in data

    def test_03_member_query(self, member_cluster):
        """Member 集群 - 审计列表"""
        res = query_auditing(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群审计列表查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data