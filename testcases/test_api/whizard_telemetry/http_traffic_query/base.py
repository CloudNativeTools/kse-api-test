from aomaker.storage import cache
from apis.whizard_telemetry.http_traffic_query.apis import (
    QueryTopologyMetricsAPI,
    QueryNodePairMetricsAPI,
    QueryServerMetricsAPI,
    QueryTrafficAPI,
)
from utils.time_helpers import make_timestamp, resolve_traffic_time_range


def query_topology_metrics(
    cluster: str = "host",
    namespace: str = "",
    metrics_filter: str = "http_topology_nodes",
    rate_interval: str = "30m",
    **extra_params,
):
    api = QueryTopologyMetricsAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.namespace = namespace
    api.query_params.time = make_timestamp(0)
    api.query_params.rate_interval = rate_interval
    api.query_params.metrics_filter = metrics_filter
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_node_pair_metrics(
    cluster: str = "host",
    server_namespace: str = "",
    metrics_filter: str = "http_node_pair_request_rate|http_node_pair_request_duration_avg",
    rate_interval: str = "30m",
    **extra_params,
):
    api = QueryNodePairMetricsAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.server_namespace = server_namespace
    api.query_params.time = make_timestamp(0)
    api.query_params.rate_interval = rate_interval
    api.query_params.metrics_filter = metrics_filter
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_server_metrics(
    cluster: str = "host",
    server_namespace: str = "",
    hours_ago: int = 1,
    step: str = "180s",
    times: int = 10,
    metrics_filter: str = "http_node_server_request_rate|http_node_server_request_error_ratio|http_node_server_request_duration_p95|http_node_server_request_duration_p99|http_node_server_request_body_bytes_rate|http_node_server_response_body_bytes_rate",
    **extra_params,
):
    tr = resolve_traffic_time_range(hours_ago)
    api = QueryServerMetricsAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.server_namespace = server_namespace
    api.query_params.start = tr["start_time"]
    api.query_params.end = tr["end_time"]
    api.query_params.step = step
    api.query_params.time = str(times)
    api.query_params.metrics_filter = metrics_filter
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_server_list(
    cluster: str = "host",
    server_namespace: str = "",
    hours_ago: int = 1,
    step: str = "180s",
    times: int = 10,
    **extra_params,
):
    tr = resolve_traffic_time_range(hours_ago)
    api = QueryServerMetricsAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.server_namespace = server_namespace
    api.query_params.start = tr["start_time"]
    api.query_params.end = tr["end_time"]
    api.query_params.step = step
    api.query_params.time = str(times)
    api.query_params.metrics_filter = "http_node_server_request_rate"
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_traffic(
    cluster: str = "host",
    hours_ago: int = 1,
    sort_field: str = "eventTimestamp",
    size: int = 10,
    **extra_params,
):
    tr = resolve_traffic_time_range(hours_ago)
    api = QueryTrafficAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.sort_field = sort_field
    api.query_params.size = size
    api.query_params.start_time = tr["start_time"]
    api.query_params.end_time = tr["end_time"]
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def get_for_test_http_traffic():
    cache_key = "http_traffic_env_ready"
    if cache.get(cache_key):
        return True
    try:
        res = query_topology_metrics()
        if res.cached_response.raw_response.status_code == 200:
            cache.set(cache_key, True)
            return True
        return False
    except Exception:
        return False


def get_first_node_name(cluster: str = "host") -> str:
    from utils.cluster_helpers import get_cluster_nodes
    nodes = get_cluster_nodes(cluster)
    return nodes[0] if nodes else ""