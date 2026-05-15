from aomaker.storage import cache
from apis.whizard_telemetry.network_traffic_query.apis import (
    QueryTopologyMetricsAPI,
    QueryNodeMetricsAPI,
    QueryNodePairMetricsAPI,
)
from utils.time_helpers import make_timestamp


def query_topology_metrics(
    cluster: str = "host",
    src_namespace: str = "",
    dst_namespace: str = "",
    metrics_filter: str = "network_topology_nodes",
    rate_interval: str = "30m",
    **extra_params,
):
    api = QueryTopologyMetricsAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.src_namespace = src_namespace
    api.query_params.dst_namespace = dst_namespace
    api.query_params.time = make_timestamp(0)
    api.query_params.rate_interval = rate_interval
    api.query_params.metrics_filter = metrics_filter
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_node_metrics(
    cluster: str = "host",
    src_namespace: str = "",
    dst_namespace: str = "",
    metrics_filter: str = "network_node_transmit_bytes_rate|network_node_receive_bytes_rate|network_node_total_bytes_rate",
    rate_interval: str = "30m",
    **extra_params,
):
    api = QueryNodeMetricsAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.src_namespace = src_namespace
    api.query_params.dst_namespace = dst_namespace
    api.query_params.time = make_timestamp(0)
    api.query_params.rate_interval = rate_interval
    api.query_params.metrics_filter = metrics_filter
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_node_pair_metrics(
    cluster: str = "host",
    src_namespace: str = "",
    dst_namespace: str = "",
    metrics_filter: str = "network_node_pair_transmit_bytes_rate|network_node_pair_receive_bytes_rate",
    rate_interval: str = "30m",
    **extra_params,
):
    api = QueryNodePairMetricsAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.src_namespace = src_namespace
    api.query_params.dst_namespace = dst_namespace
    api.query_params.time = make_timestamp(0)
    api.query_params.rate_interval = rate_interval
    api.query_params.metrics_filter = metrics_filter
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def get_for_test_network_traffic():
    cache_key = "network_traffic_env_ready"
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