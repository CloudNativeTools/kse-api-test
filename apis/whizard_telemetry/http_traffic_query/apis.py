from typing import Optional
from attrs import define, field
from .models import EbpfAPIResponse, MonitoringMetrics
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "QueryTrafficAPI",
    "QueryServerMetricsAPI",
    "QueryNodePairMetricsAPI",
    "QueryTopologyMetricsAPI",
]


@define(kw_only=True)
@router.get("/kapis/network.wiztelemetry.io/v1alpha1/http_traffic/traffic")
class QueryTrafficAPI(BaseAPI[EbpfAPIResponse]):
    """None"""

    @define
    class QueryParams:
        operation: Optional[str] = field(
            default="query",
            metadata={
                "description": "Operation type. This can be one of four types: query (for querying logs), export (for exporting logs). Defaults to query."
            },
        )
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name. e.g., 'host'"}
        )
        client_address: Optional[str] = field(
            default=None, metadata={"description": "Client address"}
        )
        client_namespace: Optional[str] = field(
            default=None, metadata={"description": "Client namespace"}
        )
        client_node_name: Optional[str] = field(
            default=None, metadata={"description": "Client node name"}
        )
        client_pod_name: Optional[str] = field(
            default=None, metadata={"description": "Client pod name"}
        )
        client_pod_name_filter: Optional[str] = field(
            default=None, metadata={"description": "Client pod name,fuzzy match"}
        )
        client_service_name: Optional[str] = field(
            default=None, metadata={"description": "Client service name"}
        )
        client_owner_name: Optional[str] = field(
            default=None, metadata={"description": "Client owner name"}
        )
        client_owner_name_filter: Optional[str] = field(
            default=None, metadata={"description": "Client owner name,fuzzy match"}
        )
        client_name: Optional[str] = field(
            default=None, metadata={"description": "Client name"}
        )
        req_method: Optional[str] = field(
            default=None, metadata={"description": "Request method"}
        )
        req_path: Optional[str] = field(
            default=None, metadata={"description": "Request path"}
        )
        resp_status_code: Optional[str] = field(
            default=None, metadata={"description": "Response status code"}
        )
        server_address: Optional[str] = field(
            default=None, metadata={"description": "Server address"}
        )
        server_namespace: Optional[str] = field(
            default=None, metadata={"description": "Server namespace"}
        )
        server_pod_name: Optional[str] = field(
            default=None, metadata={"description": "Server pod name"}
        )
        server_pod_name_filter: Optional[str] = field(
            default=None, metadata={"description": "Server pod name,fuzzy match"}
        )
        server_node_name: Optional[str] = field(
            default=None, metadata={"description": "Server node name"}
        )
        server_service_name: Optional[str] = field(
            default=None, metadata={"description": "Server service name"}
        )
        server_owner_name: Optional[str] = field(
            default=None, metadata={"description": "Server owner name"}
        )
        server_owner_name_filter: Optional[str] = field(
            default=None, metadata={"description": "Server owner name,fuzzy match"}
        )
        server_name: Optional[str] = field(
            default=None, metadata={"description": "Server name"}
        )
        src_container: Optional[str] = field(
            default=None, metadata={"description": "Source container name"}
        )
        src_container_filter: Optional[str] = field(
            default=None, metadata={"description": "Source container name,fuzzy match"}
        )
        trace_role: Optional[str] = field(
            default=None,
            metadata={"description": "Trace role, known values include Client, Server"},
        )
        start_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query. The format is a string representing seconds since the epoch, eg. 1136214245."
            },
        )
        sort_field: Optional[str] = field(
            default="RequestReceivedTimestamp",
            metadata={"description": "Sort field. One of `eventTimestamp` `duration`."},
        )
        end_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query. The format is a string representing seconds since the epoch, eg. 1136214245."
            },
        )
        sort: Optional[str] = field(
            default="desc",
            metadata={
                "description": "Sort order. One of asc, desc. This field sorts events by `RequestReceivedTimestamp`."
            },
        )
        from_: Optional[int] = field(
            default=0,
            metadata={
                "description": "The offset from the result set. This field returns query results from the specified offset. It requires **operation** is set to `query`. Defaults to 0 (i.e. from the beginning of the result set).",
                "original_name": "from",
            },
        )
        size: Optional[int] = field(
            default=10,
            metadata={
                "description": "Size of result set to return. It requires **operation** is set to `query`. Defaults to 10 (i.e. 10 event records)."
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[EbpfAPIResponse] = field(default=EbpfAPIResponse)
    endpoint_id: Optional[str] = field(default="queryTraffic")


@define(kw_only=True)
@router.get("/kapis/network.wiztelemetry.io/v1alpha1/http_traffic/server_metrics")
class QueryServerMetricsAPI(BaseAPI[MonitoringMetrics]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        server_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        server_type: Optional[str] = field(
            default=None,
            metadata={
                "description": "Http server type. one of Pod, Service, Node, IP. If not specified, all of them."
            },
        )
        server_name: Optional[str] = field(
            default=None,
            metadata={
                "description": "Http server name. May be a k8s Pod/Service/Node name, or an IP address"
            },
        )
        metrics_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The metric name filter consists of a regexp pattern. It specifies which metric data to return. For example, the following filter matches both request rate and duration average: `http_node_server_request_rate|http_node_server_request_duration_avg`. View available metrics at [kubesphere.io](https://docs.kubesphere.io/advanced-v2.0/zh-CN/api-reference/monitoring-metrics/)."
            },
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "description": "Query type. Set to `rank` for ranked results of server metrics."
            },
        )
        start: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query. Use **start** and **end** to retrieve metric data over a time span. It is a string with Unix time format, eg. 1559347200."
            },
        )
        end: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query. Use **start** and **end** to retrieve metric data over a time span. It is a string with Unix time format, eg. 1561939200."
            },
        )
        step: Optional[str] = field(
            default="10m",
            metadata={
                "description": "Time interval. Retrieve metric data at a fixed interval within the time range of start and end. It requires both **start** and **end** are provided. The format is [0-9]+[smhdwy]. Defaults to 10m (i.e. 10 min)."
            },
        )
        time: Optional[str] = field(
            default=None,
            metadata={
                "description": "A timestamp in Unix time format. Retrieve metric data at a single point in time. Defaults to now. Time and the combination of start, end, step are mutually exclusive."
            },
        )
        rate_interval: Optional[str] = field(
            default=None,
            metadata={
                "description": "Rate interval. It specifies a time range to calculate the rate of increase. The format is [0-9]+[smhdwy]."
            },
        )
        sort_metric: Optional[str] = field(
            default=None,
            metadata={
                "description": "Sort containers by the specified metric. Not applicable if **start** and **end** are provided."
            },
        )
        sort_type: Optional[str] = field(
            default="desc.",
            metadata={"description": "Sort order. One of asc, desc."},
        )
        page: Optional[int] = field(
            default=None,
            metadata={
                "description": "The page number. This field paginates result data of each metric, then returns a specific page. For example, setting **page** to 2 returns the second page. It only applies to sorted metric data."
            },
        )
        limit: Optional[int] = field(
            default=5,
            metadata={
                "description": "Page size, the maximum number of results in a single page. Defaults to 5."
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[MonitoringMetrics] = field(default=MonitoringMetrics)
    endpoint_id: Optional[str] = field(default="queryServerMetrics")


@define(kw_only=True)
@router.get("/kapis/network.wiztelemetry.io/v1alpha1/http_traffic/node_pair_metrics")
class QueryNodePairMetricsAPI(BaseAPI[MonitoringMetrics]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        type: Optional[str] = field(
            default=None,
            metadata={"description": "Query type. Set to `rank` for ranked results."},
        )
        server_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        server_type: Optional[str] = field(
            default=None,
            metadata={
                "description": "Http server type. one of Pod, Service, Node, IP. If not specified, all of them."
            },
        )
        server_name: Optional[str] = field(
            default=None,
            metadata={
                "description": "Http server name. May be a k8s Pod/Service/Node name, or an IP address"
            },
        )
        client_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        client_type: Optional[str] = field(
            default=None,
            metadata={
                "description": "Http client type. one of Pod, Service, Node, IP. If not specified, all of them."
            },
        )
        client_name: Optional[str] = field(
            default=None,
            metadata={
                "description": "Http client name. May be a k8s Pod/Service/Node name, or an IP address"
            },
        )
        metrics_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The metric name filter consists of a regexp pattern. It specifies which metric data to return. For example, the following filter matches both request rate and duration average: `http_node_pair_request_rate|http_node_pair_request_duration_avg`. View available metrics at [kubesphere.io](https://docs.kubesphere.io/advanced-v2.0/zh-CN/api-reference/monitoring-metrics/)."
            },
        )
        start: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query. Use **start** and **end** to retrieve metric data over a time span. It is a string with Unix time format, eg. 1559347200."
            },
        )
        end: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query. Use **start** and **end** to retrieve metric data over a time span. It is a string with Unix time format, eg. 1561939200."
            },
        )
        step: Optional[str] = field(
            default="10m",
            metadata={
                "description": "Time interval. Retrieve metric data at a fixed interval within the time range of start and end. It requires both **start** and **end** are provided. The format is [0-9]+[smhdwy]. Defaults to 10m (i.e. 10 min)."
            },
        )
        time: Optional[str] = field(
            default=None,
            metadata={
                "description": "A timestamp in Unix time format. Retrieve metric data at a single point in time. Defaults to now. Time and the combination of start, end, step are mutually exclusive."
            },
        )
        rate_interval: Optional[str] = field(
            default=None,
            metadata={
                "description": "Rate interval. It specifies a time range to calculate the rate of increase. The format is [0-9]+[smhdwy]."
            },
        )
        sort_metric: Optional[str] = field(
            default=None,
            metadata={
                "description": "Sort containers by the specified metric. Not applicable if **start** and **end** are provided."
            },
        )
        sort_type: Optional[str] = field(
            default="desc.",
            metadata={"description": "Sort order. One of asc, desc."},
        )
        page: Optional[int] = field(
            default=None,
            metadata={
                "description": "The page number. This field paginates result data of each metric, then returns a specific page. For example, setting **page** to 2 returns the second page. It only applies to sorted metric data."
            },
        )
        limit: Optional[int] = field(
            default=5,
            metadata={
                "description": "Page size, the maximum number of results in a single page. Defaults to 5."
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[MonitoringMetrics] = field(default=MonitoringMetrics)
    endpoint_id: Optional[str] = field(default="queryNodePairMetrics")


@define(kw_only=True)
@router.get("/kapis/network.wiztelemetry.io/v1alpha1/http_traffic/topology_metrics")
class QueryTopologyMetricsAPI(BaseAPI[MonitoringMetrics]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        metrics_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The metric name filter consists of a regexp pattern. It specifies which metric data to return. For example, the following filter matches nodes for http topology: `http_topology_nodes`. View available metrics at [kubesphere.io](https://docs.kubesphere.io/advanced-v2.0/zh-CN/api-reference/monitoring-metrics/)."
            },
        )
        start: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query. Use **start** and **end** to retrieve metric data over a time span. It is a string with Unix time format, eg. 1559347200."
            },
        )
        end: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query. Use **start** and **end** to retrieve metric data over a time span. It is a string with Unix time format, eg. 1561939200."
            },
        )
        step: Optional[str] = field(
            default="10m",
            metadata={
                "description": "Time interval. Retrieve metric data at a fixed interval within the time range of start and end. It requires both **start** and **end** are provided. The format is [0-9]+[smhdwy]. Defaults to 10m (i.e. 10 min)."
            },
        )
        time: Optional[str] = field(
            default=None,
            metadata={
                "description": "A timestamp in Unix time format. Retrieve metric data at a single point in time. Defaults to now. Time and the combination of start, end, step are mutually exclusive."
            },
        )
        rate_interval: Optional[str] = field(
            default=None,
            metadata={
                "description": "Rate interval. It specifies a time range to calculate the rate of increase. The format is [0-9]+[smhdwy]."
            },
        )
        sort_metric: Optional[str] = field(
            default=None,
            metadata={
                "description": "Sort containers by the specified metric. Not applicable if **start** and **end** are provided."
            },
        )
        sort_type: Optional[str] = field(
            default="desc.",
            metadata={"description": "Sort order. One of asc, desc."},
        )
        page: Optional[int] = field(
            default=None,
            metadata={
                "description": "The page number. This field paginates result data of each metric, then returns a specific page. For example, setting **page** to 2 returns the second page. It only applies to sorted metric data."
            },
        )
        limit: Optional[int] = field(
            default=5,
            metadata={
                "description": "Page size, the maximum number of results in a single page. Defaults to 5."
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[MonitoringMetrics] = field(default=MonitoringMetrics)
    endpoint_id: Optional[str] = field(default="queryTopologyMetrics")