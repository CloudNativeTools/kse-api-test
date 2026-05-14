import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.http_traffic_query.base import (
    query_topology_metrics,
    query_node_pair_metrics,
    query_server_metrics,
    query_traffic,
    query_server_metrics_rank,
    get_for_test_http_traffic,
)

FILTERS = load_test_data("whizard_telemetry", "http_traffic_query/data", default={})


@pytest.mark.whizard_http_traffic_scene
class TestHttpTrafficAnalysisWorkflow:
    """
    HTTP 流量分析工作流场景测试
    1. 查询拓扑节点 -> 2. 查询节点对指标 -> 3. 查询服务端指标 -> 4. 查询流量日志 -> 5. 查询排名
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_http_traffic():
            pytest.skip("HTTP 流量查询环境不可用")

    def test_01_query_topology(self):
        """步骤1: 查询 HTTP 拓扑节点"""
        ns = FILTERS.get("namespaces", {}).get("host_namespace", "kubesphere-system")
        res = query_topology_metrics(namespace=ns)
        status, text = get_http_info(res)
        assert status == 200, f"查询拓扑节点失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data, "响应中缺少 results 字段"
        self.topology_results = data.get("results", [])
        assert isinstance(self.topology_results, list)

    def test_02_query_node_pair_metrics(self):
        """步骤2: 查询 HTTP 节点对指标"""
        server_ns = FILTERS.get("namespaces", {}).get("server_namespace", "kubesphere-system")
        res = query_node_pair_metrics(server_namespace=server_ns)
        status, text = get_http_info(res)
        assert status == 200, f"查询节点对指标失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data, "响应中缺少 results 字段"
        self.node_pair_results = data.get("results", [])
        assert isinstance(self.node_pair_results, list)

    def test_03_query_server_metrics(self):
        """步骤3: 查询服务端指标"""
        server_ns = FILTERS.get("namespaces", {}).get("server_namespace", "kubesphere-system")
        res = query_server_metrics(server_namespace=server_ns)
        status, text = get_http_info(res)
        assert status == 200, f"查询服务端指标失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data, "响应中缺少 results 字段"
        self.server_metrics = data.get("results", [])
        assert isinstance(self.server_metrics, list)

    def test_04_query_traffic_logs(self):
        """步骤4: 查询 HTTP 流量日志"""
        res = query_traffic(size=20)
        status, text = get_http_info(res)
        assert status == 200, f"查询流量日志失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data, "响应中缺少 query 字段"
        query_data = data.get("query", {})
        self.traffic_data = query_data.get("records", [])
        self.traffic_total = query_data.get("total", 0)
        assert isinstance(self.traffic_total, int)

    def test_05_query_server_rank(self):
        """步骤5: 查询服务端指标排名"""
        service = FILTERS.get("service_traffic", {})
        server_ns = service.get("server_namespace", "kubesphere-system")
        server_name = service.get("server_name", "ks-apiserver")
        res = query_server_metrics_rank(
            server_namespace=server_ns,
            server_name=server_name,
        )
        status, text = get_http_info(res)
        assert status == 200, f"查询服务端排名失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data, "响应中缺少 results 字段"
        self.rank_results = data.get("results", [])
        assert isinstance(self.rank_results, list)

    def test_06_filter_traffic_by_method(self):
        """步骤6: 按请求方法过滤流量日志"""
        method = FILTERS.get("traffic_filters", {}).get("by_method", {}).get("req_method", "POST")
        res = query_traffic(req_method=method)
        status, text = get_http_info(res)
        assert status == 200, f"按请求方法过滤失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data.get("query", {}).get("records", [])
        for record in records:
            msg = record.get("message", {})
            actual_method = msg.get("req_method", "")
            assert actual_method == method, \
                f"期望 req_method={method}，实际: {actual_method}"

    def test_07_filter_traffic_by_status_code(self):
        """步骤7: 按响应状态码过滤流量日志"""
        status_code = int(FILTERS.get("traffic_filters", {}).get("by_status_code", {}).get("resp_status_code", "200"))
        res = query_traffic(resp_status_code=str(status_code))
        status, text = get_http_info(res)
        assert status == 200, f"按状态码过滤失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        records = data.get("query", {}).get("records", [])
        for record in records:
            msg = record.get("message", {})
            actual_code = msg.get("resp_status_code")
            assert actual_code == status_code, \
                f"期望 resp_status_code={status_code}，实际: {actual_code}"


@pytest.mark.whizard_http_traffic_scene
@pytest.mark.multi_cluster
class TestHttpTrafficMultiClusterComparison:
    """
    多集群 HTTP 流量对比场景测试

    验证 Member 集群的 HTTP 流量查询均正常
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_http_traffic():
            pytest.skip("HTTP 流量查询环境不可用")

    def test_01_member_topology(self, member_cluster):
        """Member 集群 - 拓扑节点"""
        res = query_topology_metrics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群拓扑查询失败: {status}, {text}"

    def test_02_member_node_pair(self, member_cluster):
        """Member 集群 - 节点对指标"""
        res = query_node_pair_metrics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群节点对查询失败: {status}, {text}"

    def test_03_member_server_metrics(self, member_cluster):
        """Member 集群 - 服务端指标"""
        res = query_server_metrics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群服务端指标查询失败: {status}, {text}"

    def test_04_member_traffic_logs(self, member_cluster):
        """Member 集群 - 流量日志"""
        res = query_traffic(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群流量日志查询失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data

    def test_05_member_server_rank(self, member_cluster):
        """Member 集群 - 服务端排名"""
        res = query_server_metrics_rank(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群服务端排名查询失败: {status}, {text}"