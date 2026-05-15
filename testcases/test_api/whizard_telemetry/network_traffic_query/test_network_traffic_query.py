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
TOPOLOGY = FILTERS.get("topology", {})
NODE_METRICS = FILTERS.get("node_metrics", {})
NODE_PAIR_METRICS = FILTERS.get("node_pair_metrics", {})
RANK = FILTERS.get("rank", {})
NAMESPACES = FILTERS.get("namespaces", {})
INVALID_PARAMS = FILTERS.get("invalid_params", {})
CLUSTERS = FILTERS.get("clusters", {})


@pytest.mark.whizard_network_traffic
class TestNetworkTopology:
    """网络拓扑查询"""

    def test_topology_success(self):
        """查询网络拓扑节点 - 成功"""
        res = query_topology_metrics(
            metrics_filter=TOPOLOGY.get("metrics_filter", "network_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_topology_with_src_namespace(self):
        """查询网络拓扑 - 按源项目过滤"""
        src_ns = NAMESPACES.get("src", "kubesphere-monitoring-system")
        res = query_topology_metrics(
            src_namespace=src_ns,
            metrics_filter=TOPOLOGY.get("metrics_filter", "network_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_topology_with_dst_namespace(self):
        """查询网络拓扑 - 按目标项目过滤"""
        dst_ns = NAMESPACES.get("dst", "kubesphere-system")
        res = query_topology_metrics(
            dst_namespace=dst_ns,
            metrics_filter=TOPOLOGY.get("metrics_filter", "network_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_topology_with_both_namespaces(self):
        """查询网络拓扑 - 按源和目标项目过滤"""
        src_ns = NAMESPACES.get("src", "kubesphere-monitoring-system")
        dst_ns = NAMESPACES.get("dst", "kubesphere-system")
        res = query_topology_metrics(
            src_namespace=src_ns,
            dst_namespace=dst_ns,
            metrics_filter=TOPOLOGY.get("metrics_filter", "network_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_topology_with_2h_interval(self):
        """查询网络拓扑 - 2小时间隔"""
        res = query_topology_metrics(
            rate_interval="2h",
            metrics_filter=TOPOLOGY.get("metrics_filter", "network_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_topology_with_daily_interval(self):
        """查询网络拓扑 - 按天查询"""
        res = query_topology_metrics(
            rate_interval="3d",
            metrics_filter=TOPOLOGY.get("metrics_filter", "network_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_network_traffic
class TestNetworkNodeMetrics:
    """网络资源流量查询"""

    def test_node_metrics_success(self):
        """查询资源各流量指标 - 成功"""
        res = query_node_metrics(
            metrics_filter=NODE_METRICS.get(
                "metrics_filter",
                "network_node_transmit_bytes_rate|network_node_receive_bytes_rate|network_node_total_bytes_rate",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_node_metrics_single_metric(self):
        """查询资源流量 - 仅查询单个指标"""
        res = query_node_metrics(
            metrics_filter="network_node_transmit_bytes_rate",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_node_metrics_with_namespace(self):
        """查询资源流量 - 按命名空间过滤"""
        src_ns = NAMESPACES.get("src", "kubesphere-monitoring-system")
        res = query_node_metrics(
            src_namespace=src_ns,
            metrics_filter=NODE_METRICS.get(
                "metrics_filter",
                "network_node_transmit_bytes_rate|network_node_receive_bytes_rate|network_node_total_bytes_rate",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_network_traffic
class TestNetworkNodePairMetrics:
    """网络资源起点->终点流量查询"""

    def test_node_pair_success(self):
        """查询起点->终点流量 - 成功"""
        res = query_node_pair_metrics(
            metrics_filter=NODE_PAIR_METRICS.get(
                "metrics_filter",
                "network_node_pair_transmit_bytes_rate|network_node_pair_receive_bytes_rate",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_node_pair_with_namespace(self):
        """查询起点->终点流量 - 按命名空间过滤"""
        src_ns = NAMESPACES.get("src", "kubesphere-monitoring-system")
        dst_ns = NAMESPACES.get("dst", "kubesphere-system")
        res = query_node_pair_metrics(
            src_namespace=src_ns,
            dst_namespace=dst_ns,
            metrics_filter=NODE_PAIR_METRICS.get(
                "metrics_filter",
                "network_node_pair_transmit_bytes_rate|network_node_pair_receive_bytes_rate",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_network_traffic
class TestNetworkRank:
    """网络流量rank排名查询"""

    def test_rank_success(self):
        """查询流量rank排名 - 成功"""
        res = query_node_pair_metrics(
            type=RANK.get("type", "rank"),
            sort_type=RANK.get("sort_type", "desc"),
            sort_metric=RANK.get("sort_metric", "network_node_pair_transmit_bytes_rate"),
            page=RANK.get("page", 1),
            limit=RANK.get("limit", 10),
            metrics_filter=RANK.get(
                "metrics_filter",
                "network_node_pair_transmit_bytes_rate|network_node_pair_receive_bytes_rate|network_node_pair_total_bytes_rate|network_node_pair_tcp_retrans_packets_rate|network_node_pair_tcp_drops_packets_rate",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data

    def test_rank_ascending(self):
        """查询流量rank排名 - 升序"""
        res = query_node_pair_metrics(
            type="rank",
            sort_type="asc",
            sort_metric="network_node_pair_transmit_bytes_rate",
            page=1,
            limit=10,
            metrics_filter="network_node_pair_transmit_bytes_rate|network_node_pair_receive_bytes_rate",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_rank_second_page(self):
        """查询流量rank排名 - 第二页"""
        res = query_node_pair_metrics(
            type="rank",
            sort_type="desc",
            sort_metric="network_node_pair_transmit_bytes_rate",
            page=2,
            limit=5,
            metrics_filter="network_node_pair_transmit_bytes_rate|network_node_pair_receive_bytes_rate",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_rank_with_tcp_metrics(self):
        """查询流量rank排名 - 含TCP重传/丢包指标"""
        res = query_node_pair_metrics(
            type="rank",
            sort_type="desc",
            sort_metric="network_node_pair_tcp_retrans_packets_rate",
            page=1,
            limit=10,
            metrics_filter="network_node_pair_tcp_retrans_packets_rate|network_node_pair_tcp_drops_packets_rate",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_network_traffic
@pytest.mark.multi_cluster
class TestNetworkTrafficMemberCluster:
    """Member集群 - 网络流量查询"""

    def _verify_member_cluster(self, data, member_cluster):
        """校验数据来源于member集群"""
        results = data.get("results") or []
        if not results:
            return
        metric_data = results[0].get("data")
        if not metric_data:
            return
        result_items = metric_data.get("result") or []
        if not result_items:
            return
        cluster_label = result_items[0].get("metric", {}).get("cluster", "")
        assert cluster_label == member_cluster, (
            f"cluster label mismatch: expected '{member_cluster}', got '{cluster_label}'"
        )

    def test_member_topology(self, member_cluster):
        """Member集群 - 查询网络拓扑"""
        member_cfg = CLUSTERS.get("member", {})
        res = query_topology_metrics(
            cluster=member_cluster,
            src_namespace=member_cfg.get("src_namespace", ""),
            dst_namespace=member_cfg.get("dst_namespace", ""),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data
        self._verify_member_cluster(data, member_cluster)

    def test_member_node_metrics(self, member_cluster):
        """Member集群 - 查询资源流量"""
        res = query_node_metrics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        self._verify_member_cluster(data, member_cluster)

    def test_member_node_pair(self, member_cluster):
        """Member集群 - 查询起点->终点流量"""
        res = query_node_pair_metrics(cluster=member_cluster)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        self._verify_member_cluster(data, member_cluster)

    def test_member_rank(self, member_cluster):
        """Member集群 - 查询流量rank排名"""
        res = query_node_pair_metrics(
            cluster=member_cluster,
            type="rank",
            sort_type="desc",
            sort_metric="network_node_pair_transmit_bytes_rate",
            page=1,
            limit=10,
            metrics_filter="network_node_pair_transmit_bytes_rate|network_node_pair_receive_bytes_rate",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        self._verify_member_cluster(data, member_cluster)


@pytest.mark.whizard_network_traffic
class TestNetworkTrafficEdgeCases:
    """网络流量边界场景"""

    def test_invalid_metric_filter(self):
        """无效的指标过滤 - 应返回空结果"""
        res = query_topology_metrics(
            metrics_filter=INVALID_PARAMS.get("invalid_metric", "nonexistent_metric"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}"
        data = res.cached_response.raw_response.json()
        assert data.get("results") is None
        assert data.get("total_item") == 0

    def test_empty_namespace_filter(self):
        """空命名空间过滤 - 应返回所有命名空间数据"""
        res = query_topology_metrics(src_namespace="", dst_namespace="")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"