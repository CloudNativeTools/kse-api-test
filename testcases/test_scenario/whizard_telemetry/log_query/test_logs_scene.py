import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.log_query.base import (
    query_logs,
    query_logs_statistics,
    query_logs_histogram,
    get_for_test_logs,
)

FILTERS = load_test_data("whizard_telemetry", "log_query/logs", "filters", default={})
PAGINATION = load_test_data("whizard_telemetry", "log_query/logs", "pagination", default={})


@pytest.mark.whizard_logs_scene
class TestLogsAnalysisWorkflow:
    """
    日志分析工作流场景测试
    1. 获取统计概览 -> 2. 获取直方图趋势 -> 3. 查询最近日志列表
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_logs():
            pytest.skip("日志查询环境不可用")

    def test_01_get_statistics_overview(self):
        """步骤1: 获取日志统计概览"""
        res = query_logs_statistics()
        status, text = get_http_info(res)
        assert status == 200, f"查询日志统计失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "statistics" in data, "响应中缺少 statistics 字段"
        self.stat_containers = data["statistics"].get("containers", 0)
        self.stat_logs = data["statistics"].get("logs", 0)
        assert isinstance(self.stat_containers, int)
        assert isinstance(self.stat_logs, int)

    def test_02_get_histogram_trend(self):
        """步骤2: 获取日志直方图趋势"""
        res = query_logs_histogram()
        status, text = get_http_info(res)
        assert status == 200, f"查询日志直方图失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "histogram" in data, "响应中缺少 histogram 字段"
        histogram = data["histogram"]
        assert "total" in histogram
        assert "histograms" in histogram
        assert isinstance(histogram["total"], int)
        assert isinstance(histogram["histograms"], list)

    def test_03_query_recent_logs(self):
        """步骤3: 查询最近日志列表"""
        res = query_logs(size=50)
        status, text = get_http_info(res)
        assert status == 200, f"查询日志列表失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data, "响应中缺少 query 字段"
        self.total_logs = data["query"].get("total", 0)
        self.records = data["query"].get("records") or []
        assert isinstance(self.total_logs, int)

    def test_04_filter_by_namespace(self, test_namespace):
        """步骤4: 按命名空间过滤查询"""
        res = query_logs(namespaces=test_namespace)
        status, text = get_http_info(res)
        assert status == 200, f"按命名空间过滤查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        for record in records:
            assert record.get("namespace") == test_namespace, \
                f"期望 namespace={test_namespace}，实际: {record.get('namespace')}"

    def test_05_filter_by_workload(self, test_namespace):
        """步骤5: 按工作负载过滤查询"""
        workloads = FILTERS.get("workload_filter", {}).get("workloads", "host-nginx")
        res = query_logs(
            namespaces=test_namespace,
            workloads=workloads,
        )
        status, text = get_http_info(res)
        assert status == 200, f"按工作负载过滤查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        for record in records:
            assert record.get("namespace") == test_namespace, \
                f"期望 namespace={test_namespace}，实际: {record.get('namespace')}"

    def test_06_filter_by_pod_and_container(self, test_namespace):
        """步骤6: 组合 Pod 和容器过滤"""
        pods = FILTERS.get("pod_filter", {}).get("pods", "host-nginx")
        containers = FILTERS.get("container_filter", {}).get("containers", "nginx")
        res = query_logs(
            namespaces=test_namespace,
            pod_query=pods,
            container_query=containers,
        )
        status, text = get_http_info(res)
        assert status == 200, f"组合过滤查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        for record in records:
            assert record.get("namespace") == test_namespace
            assert pods in record.get("pod"), \
                f"期望 pod 包含 {pods}，实际: {record.get('pod')}"
            assert containers in record.get("container"), \
                f"期望 container 包含 {containers}，实际: {record.get('container')}"

    def test_07_search_log_content(self):
        """步骤7: 按日志内容搜索"""
        log_query = FILTERS.get("log_query", {}).get("log_query", "INFO")
        res = query_logs(log_query=log_query)
        status, text = get_http_info(res)
        assert status == 200, f"按日志内容搜索失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        for record in records:
            log_text = record.get("log", "").upper()
            assert log_query.upper() in log_text, \
                f"期望 log 包含 {log_query}，实际: {record.get('log')}"

    def test_08_pagination_across_pages(self):
        """步骤8: 分页查询验证"""
        page_1 = PAGINATION.get("page_1", {"from": 0, "size": 5})
        page_2 = PAGINATION.get("page_2", {"from": 5, "size": 5})
        res_page1 = query_logs(time_range_key="last_3h", from_=page_1["from"], size=page_1["size"])
        status1, _ = get_http_info(res_page1)
        assert status1 == 200
        data1 = res_page1.cached_response.raw_response.json()

        res_page2 = query_logs(time_range_key="last_3h", from_=page_2["from"], size=page_2["size"])
        status2, _ = get_http_info(res_page2)
        assert status2 == 200
        data2 = res_page2.cached_response.raw_response.json()

        records1 = data1["query"].get("records") or []
        records2 = data2["query"].get("records") or []

        total = data1["query"].get("total", 0)
        if records1 and records2 and total > 5:
            assert records1 != records2, "两页数据完全相同，分页可能未生效"


@pytest.mark.whizard_logs_scene
@pytest.mark.multi_cluster
class TestLogsMultiClusterComparison:
    """
    多集群日志对比场景测试

    验证 Member 集群的日志查询均正常
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_logs():
            pytest.skip("日志查询环境不可用")

    def test_01_member_statistics(self, member_cluster):
        """Member 集群 - 日志统计"""
        res = query_logs_statistics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群统计查询失败: {status}, {text}"
        member_data = res.cached_response.raw_response.json()
        self.member_logs = member_data["statistics"].get("logs", 0)

    def test_02_member_histogram(self, member_cluster):
        """Member 集群 - 日志直方图"""
        res = query_logs_histogram(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群直方图查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "histogram" in data

    def test_03_member_query(self, member_cluster):
        """Member 集群 - 日志列表"""
        res = query_logs(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群日志列表查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data