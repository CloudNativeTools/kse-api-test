import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.http_traffic_query.base import (
    query_topology_metrics,
    query_node_pair_metrics,
    query_server_metrics,
    query_server_list,
    query_traffic,
    get_for_test_http_traffic,
    get_first_node_name,
)

FILTERS = load_test_data("whizard_telemetry", "http_traffic_query/data", default={})
TOPOLOGY = FILTERS.get("topology", {})
NODE_PAIR = FILTERS.get("node_pair", {})
RANK = FILTERS.get("rank", {})
SERVER_METRICS = FILTERS.get("server_metrics", {})
NAMESPACES = FILTERS.get("namespaces", {})
TRAFFIC_FILTERS = FILTERS.get("traffic_filters", {})
CLUSTERS = FILTERS.get("clusters", {})


@pytest.mark.whizard_http_traffic
class TestHttpTopology:
    """HTTP服务拓扑查询"""

    def test_topology_success(self):
        """查询服务拓扑节点 - 成功"""
        res = query_topology_metrics(
            metrics_filter=TOPOLOGY.get("metrics_filter", "http_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_topology_with_namespace(self):
        """查询服务拓扑 - 按项目过滤"""
        ns = NAMESPACES.get("host_namespace", "kubesphere-system")
        res = query_topology_metrics(
            namespace=ns,
            metrics_filter=TOPOLOGY.get("metrics_filter", "http_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_topology_with_3h_interval(self):
        """查询服务拓扑 - 3小时间隔"""
        res = query_topology_metrics(
            rate_interval="3h",
            metrics_filter=TOPOLOGY.get("metrics_filter", "http_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_topology_with_daily_interval(self):
        """查询服务拓扑 - 按天查询"""
        res = query_topology_metrics(
            rate_interval="3d",
            metrics_filter=TOPOLOGY.get("metrics_filter", "http_topology_nodes"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_http_traffic
class TestHttpNodePairMetrics:
    """HTTP服务拓扑起点->终点查询"""

    def test_node_pair_success(self):
        """查询服务拓扑起点->终点指标 - 成功"""
        res = query_node_pair_metrics(
            metrics_filter=NODE_PAIR.get(
                "metrics_filter",
                "http_node_pair_request_rate|http_node_pair_request_duration_avg",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data

    def test_node_pair_with_namespace(self):
        """查询服务拓扑起点->终点 - 按项目过滤"""
        ns = NAMESPACES.get("server_namespace", "kubesphere-system")
        res = query_node_pair_metrics(
            server_namespace=ns,
            metrics_filter=NODE_PAIR.get(
                "metrics_filter",
                "http_node_pair_request_rate|http_node_pair_request_duration_avg",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_http_traffic
class TestHttpRank:
    """HTTP流量rank排名查询"""

    def test_rank_success(self):
        """查询HTTP rank排名 - 成功"""
        res = query_node_pair_metrics(
            type=RANK.get("type", "rank"),
            sort_type=RANK.get("sort_type", "desc"),
            sort_metric=RANK.get("sort_metric", "http_node_pair_request_rate_by_path"),
            page=RANK.get("page", 1),
            limit=RANK.get("limit", 10),
            metrics_filter=RANK.get(
                "metrics_filter",
                "http_node_pair_request_rate_by_path|http_node_pair_request_error_ratio_by_path|http_node_pair_request_duration_p95_by_path|http_node_pair_request_duration_p99_by_path|http_node_pair_request_body_bytes_rate_by_path|http_node_pair_response_body_bytes_rate_by_path",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data

    def test_rank_ascending(self):
        """查询HTTP rank排名 - 升序"""
        res = query_node_pair_metrics(
            type="rank",
            sort_type="asc",
            sort_metric="http_node_pair_request_rate_by_path",
            page=1,
            limit=10,
            metrics_filter="http_node_pair_request_rate_by_path|http_node_pair_request_duration_p95_by_path",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_rank_second_page(self):
        """查询HTTP rank排名 - 第二页"""
        res = query_node_pair_metrics(
            type="rank",
            sort_type="desc",
            sort_metric="http_node_pair_request_rate_by_path",
            page=2,
            limit=5,
            metrics_filter="http_node_pair_request_rate_by_path|http_node_pair_request_duration_p95_by_path",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_rank_with_error_ratio(self):
        """查询HTTP rank排名 - 按错误率排序"""
        res = query_node_pair_metrics(
            type="rank",
            sort_type="desc",
            sort_metric="http_node_pair_request_error_ratio_by_path",
            page=1,
            limit=10,
            metrics_filter="http_node_pair_request_rate_by_path|http_node_pair_request_error_ratio_by_path",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_http_traffic
class TestHttpServerMetrics:
    """HTTP服务监控查询"""

    def test_server_metrics_full(self):
        """查询服务监控全指标 - 成功"""
        res = query_server_metrics(
            metrics_filter=SERVER_METRICS.get(
                "metrics_filter",
                "http_node_server_request_rate|http_node_server_request_error_ratio|http_node_server_request_duration_p95|http_node_server_request_duration_p99|http_node_server_request_body_bytes_rate|http_node_server_response_body_bytes_rate",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data

    def test_server_metrics_single(self):
        """查询服务监控 - 仅查询请求率"""
        res = query_server_metrics(
            metrics_filter="http_node_server_request_rate",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data

    def test_server_metrics_with_namespace(self):
        """查询服务监控 - 按项目过滤"""
        ns = NAMESPACES.get("server_namespace", "kubesphere-system")
        res = query_server_metrics(
            server_namespace=ns,
            metrics_filter=SERVER_METRICS.get(
                "metrics_filter",
                "http_node_server_request_rate|http_node_server_request_error_ratio|http_node_server_request_duration_p95|http_node_server_request_duration_p99|http_node_server_request_body_bytes_rate|http_node_server_response_body_bytes_rate",
            ),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_server_metrics_custom_step(self):
        """查询服务监控 - 自定义时间步长"""
        res = query_server_metrics(
            step="360s",
            times=10,
            metrics_filter="http_node_server_request_rate",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_server_list_success(self):
        """查询服务列表 - 成功"""
        res = query_server_list()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data

    def test_server_list_with_namespace(self):
        """查询服务列表 - 按项目过滤"""
        ns = NAMESPACES.get("server_namespace", "kubesphere-system")
        res = query_server_list(server_namespace=ns)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_http_traffic
class TestHttpTrafficLogs:
    """HTTP流量日志查询"""

    def test_traffic_success(self):
        """查询HTTP流量日志 - 成功"""
        res = query_traffic()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data
        assert "total" in data["query"]
        assert "records" in data["query"]

    def test_traffic_with_pagination(self):
        """查询HTTP流量日志 - 分页"""
        res = query_traffic(from_=0, size=5)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        records = data["query"].get("records") or []
        assert len(records) <= 5

    def test_traffic_filter_by_name(self):
        """查询HTTP流量日志 - 按名称过滤"""
        name_filter = TRAFFIC_FILTERS.get("by_name", {})
        res = query_traffic(
            client_name=name_filter.get("client_name", "ks-apiserver"),
            server_name=name_filter.get("server_name", "ks-apiserver"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traffic_filter_by_workload(self):
        """查询HTTP流量日志 - 按工作负载过滤"""
        wl_filter = TRAFFIC_FILTERS.get("by_workload", {})
        res = query_traffic(
            client_owner_name_filter=wl_filter.get("client_owner_name_filter", "ks-console"),
            server_owner_name_filter=wl_filter.get("server_owner_name_filter", "ks-console"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traffic_filter_by_service(self):
        """查询HTTP流量日志 - 按服务过滤"""
        svc_filter = TRAFFIC_FILTERS.get("by_service", {})
        res = query_traffic(
            client_service_name=svc_filter.get("client_service_name", "ks-console"),
            server_service_name=svc_filter.get("server_service_name", "ks-console"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traffic_filter_by_pod(self):
        """查询HTTP流量日志 - 按容器组过滤"""
        pod_filter = TRAFFIC_FILTERS.get("by_pod", {})
        res = query_traffic(
            client_pod_name_filter=pod_filter.get("client_pod_name_filter", "ks-console"),
            server_pod_name_filter=pod_filter.get("server_pod_name_filter", "ks-console"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traffic_filter_by_node(self):
        """查询HTTP流量日志 - 按节点过滤"""
        node_name = get_first_node_name()
        if not node_name:
            node_filter = TRAFFIC_FILTERS.get("by_node", {})
            node_name = node_filter.get("client_node_name", "node3")
        res = query_traffic(
            client_node_name=node_name,
            server_node_name=node_name,
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traffic_filter_by_method(self):
        """查询HTTP流量日志 - 按请求方法过滤"""
        method_filter = TRAFFIC_FILTERS.get("by_method", {})
        res = query_traffic(
            req_method=method_filter.get("req_method", "POST"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traffic_filter_by_path(self):
        """查询HTTP流量日志 - 按请求路径过滤"""
        path_filter = TRAFFIC_FILTERS.get("by_path", {})
        res = query_traffic(
            req_path=path_filter.get("req_path", "/proxy/posthog/e/"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traffic_filter_by_status_code(self):
        """查询HTTP流量日志 - 按状态码过滤"""
        status_filter = TRAFFIC_FILTERS.get("by_status_code", {})
        res = query_traffic(
            resp_status_code=status_filter.get("resp_status_code", "200"),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_http_traffic
@pytest.mark.multi_cluster
class TestHttpTrafficMemberCluster:
    """Member集群 - HTTP流量查询"""

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
        """Member集群 - 查询服务拓扑"""
        member_cfg = CLUSTERS.get("member", {})
        res = query_topology_metrics(
            cluster=member_cluster,
            namespace=member_cfg.get("namespace", ""),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "results" in data
        self._verify_member_cluster(data, member_cluster)

    def test_member_node_pair(self, member_cluster):
        """Member集群 - 查询服务拓扑起点->终点"""
        member_cfg = CLUSTERS.get("member", {})
        res = query_node_pair_metrics(
            cluster=member_cluster,
            server_namespace=member_cfg.get("namespace", ""),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        self._verify_member_cluster(data, member_cluster)

    def test_member_server_metrics(self, member_cluster):
        """Member集群 - 查询服务监控"""
        member_cfg = CLUSTERS.get("member", {})
        res = query_server_metrics(
            cluster=member_cluster,
            server_namespace=member_cfg.get("namespace", ""),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        self._verify_member_cluster(data, member_cluster)

    def test_member_traffic(self, member_cluster):
        """Member集群 - 查询HTTP流量日志"""
        member_cfg = CLUSTERS.get("member", {})
        res = query_traffic(
            cluster=member_cluster,
            client_namespace=member_cfg.get("namespace", ""),
            server_namespace=member_cfg.get("namespace", ""),
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "query" in data
        records = data["query"].get("records") or []
        if records:
            cluster_label = records[0].get("cluster", "")
            assert cluster_label == member_cluster, (
                f"cluster mismatch: expected '{member_cluster}', got '{cluster_label}'"
            )

    def test_member_rank(self, member_cluster):
        """Member集群 - 查询HTTP rank排名"""
        member_cfg = CLUSTERS.get("member", {})
        res = query_node_pair_metrics(
            cluster=member_cluster,
            server_namespace=member_cfg.get("namespace", ""),
            type="rank",
            sort_type="desc",
            sort_metric="http_node_pair_request_rate_by_path",
            page=1,
            limit=10,
            metrics_filter="http_node_pair_request_rate_by_path",
        )
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        self._verify_member_cluster(data, member_cluster)