import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.network_traffic_query.base import (
    query_topology_metrics,
    query_node_metrics,
    query_node_pair_metrics,
    get_for_test_network_traffic,
)

FILTERS = load_test_data("whizard_telemetry", "network_traffic_query/data", default={})


@pytest.mark.whizard_network_traffic_scene
class TestNetworkTrafficAnalysisWorkflow:
    """
    网络流量分析工作流场景测试
    1. 查询拓扑节点 -> 2. 查询节点指标 -> 3. 查询节点对指标
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_network_traffic():
            pytest.skip("网络流量查询环境不可用")

    def test_01_query_topology(self):
        """步骤1: 查询网络拓扑节点"""
        src_ns = FILTERS.get("namespaces", {}).get("src", "kubesphere-monitoring-system")
        dst_ns = FILTERS.get("namespaces", {}).get("dst", "kubesphere-system")
        res = query_topology_metrics(src_namespace=src_ns, dst_namespace=dst_ns)
        status, text = get_http_info(res)
        assert status == 200, f"查询拓扑节点失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data, "响应中缺少 results 字段"
        self.topology_results = data.get("results", [])
        assert isinstance(self.topology_results, list)

    def test_02_query_node_metrics(self):
        """步骤2: 查询网络节点指标"""
        src_ns = FILTERS.get("namespaces", {}).get("src", "kubesphere-monitoring-system")
        dst_ns = FILTERS.get("namespaces", {}).get("dst", "kubesphere-system")
        res = query_node_metrics(src_namespace=src_ns, dst_namespace=dst_ns)
        status, text = get_http_info(res)
        assert status == 200, f"查询节点指标失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data, "响应中缺少 results 字段"
        self.node_metrics_results = data.get("results", [])
        assert isinstance(self.node_metrics_results, list)

    def test_03_query_node_pair_metrics(self):
        """步骤3: 查询网络节点对指标"""
        src_ns = FILTERS.get("namespaces", {}).get("src", "kubesphere-monitoring-system")
        dst_ns = FILTERS.get("namespaces", {}).get("dst", "kubesphere-system")
        res = query_node_pair_metrics(src_namespace=src_ns, dst_namespace=dst_ns)
        status, text = get_http_info(res)
        assert status == 200, f"查询节点对指标失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data, "响应中缺少 results 字段"
        self.node_pair_results = data.get("results", [])
        assert isinstance(self.node_pair_results, list)

    def test_04_filter_by_single_namespace(self):
        """步骤4: 按源命名空间过滤拓扑"""
        src_ns = FILTERS.get("namespaces", {}).get("src", "kubesphere-monitoring-system")
        res = query_topology_metrics(src_namespace=src_ns)
        status, text = get_http_info(res)
        assert status == 200, f"按源命名空间过滤拓扑失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data

    def test_05_rank_node_pair_metrics(self):
        """步骤5: 查询网络节点对排名"""
        res = query_node_pair_metrics(metrics_filter="network_node_pair_transmit_bytes_rate")
        status, text = get_http_info(res)
        assert status == 200, f"查询节点对排名失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data


@pytest.mark.whizard_network_traffic_scene
@pytest.mark.multi_cluster
class TestNetworkTrafficMultiClusterComparison:
    """
    多集群网络流量对比场景测试

    验证 Member 集群的网络流量查询均正常
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_network_traffic():
            pytest.skip("网络流量查询环境不可用")

    def test_01_member_topology(self, member_cluster):
        """Member 集群 - 拓扑节点"""
        res = query_topology_metrics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群拓扑查询失败: {status}, {text}"

    def test_02_member_node_metrics(self, member_cluster):
        """Member 集群 - 节点指标"""
        res = query_node_metrics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群节点指标查询失败: {status}, {text}"

    def test_03_member_node_pair(self, member_cluster):
        """Member 集群 - 节点对指标"""
        res = query_node_pair_metrics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"Member 集群节点对查询失败: {status}, {text}"