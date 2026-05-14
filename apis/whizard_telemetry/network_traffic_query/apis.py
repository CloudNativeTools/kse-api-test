from typing import Optional
from attrs import define, field
from .models import MonitoringMetrics
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "QueryNodeMetricsAPI",
    "QueryNodePairMetricsAPI",
    "QueryTopologyMetricsAPI",
]


@define(kw_only=True)
@router.get("/kapis/network.wiztelemetry.io/v1alpha1/network_traffic/node_metrics")
class QueryNodeMetricsAPI(BaseAPI[MonitoringMetrics]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        src_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        dst_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        metrics_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The metric name filter consists of a regexp pattern. It specifies which metric data to return. For example, the following filter matches both receive rate and transmit rate: `network_node_receive_bytes_rate|network_node_transmit_bytes_rate`. View available metrics at [kubesphere.io](https://docs.kubesphere.io/advanced-v2.0/zh-CN/api-reference/monitoring-metrics/)."
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
    endpoint_id: Optional[str] = field(default="queryNodeMetrics")


@define(kw_only=True)
@router.get("/kapis/network.wiztelemetry.io/v1alpha1/network_traffic/node_pair_metrics")
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
        src_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        dst_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        metrics_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The metric name filter consists of a regexp pattern. It specifies which metric data to return. For example, the following filter matches both receive rate and transmit rate: `network_node_pair_receive_bytes_rate|network_node_pair_transmit_bytes_rate`. View available metrics at [kubesphere.io](https://docs.kubesphere.io/advanced-v2.0/zh-CN/api-reference/monitoring-metrics/)."
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
@router.get("/kapis/network.wiztelemetry.io/v1alpha1/network_traffic/topology_metrics")
class QueryTopologyMetricsAPI(BaseAPI[MonitoringMetrics]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        src_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        dst_namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        metrics_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The metric name filter consists of a regexp pattern. It specifies which metric data to return. For example, the following filter matches nodes for network topology: `network_topology_nodes`. View available metrics at [kubesphere.io](https://docs.kubesphere.io/advanced-v2.0/zh-CN/api-reference/monitoring-metrics/)."
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