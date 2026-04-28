from typing import Optional
from attrs import define, field
from .models import MonitoringMetrics
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = ["HandlePodMetricsQueryAPI"]


@define(kw_only=True)
@router.get("/kapis/monitoring.kubesphere.io/v1beta1/pod_metrics")
class HandlePodMetricsQueryAPI(BaseAPI[MonitoringMetrics]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        cluster_resources_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The cluster filter consists of a regexp pattern. It specifies which cluster data to return."
            },
        )
        node: Optional[str] = field(
            default=None, metadata={"description": "Node name."}
        )
        node_resources_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The node filter consists of a regexp pattern. It specifies which node data to return."
            },
        )
        worksapce: Optional[str] = field(
            default=None, metadata={"description": "Workspace name."}
        )
        workspace_resources_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The workspace filter consists of a regexp pattern. It specifies which workspace data to return.`."
            },
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        namespace_resources_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The namespace filter consists of a regexp pattern. It specifies which namespace data to return."
            },
        )
        workload_name: Optional[str] = field(
            default=None, metadata={"description": "Workload name."}
        )
        workload_resources_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The workload name filter consists of a regexp pattern. It specifies which workload name data to return."
            },
        )
        pod: Optional[str] = field(default=None, metadata={"description": "Pod name."})
        resources_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The pod filter consists of a regexp pattern. It specifies which pod data to return."
            },
        )
        ip: Optional[str] = field(
            default=None, metadata={"description": "Pod IP address."}
        )
        phase: Optional[str] = field(
            default=None,
            metadata={
                "description": "Pod phase. One of Pending, Running, Succeeded, Failed, Unknown."
            },
        )
        qos_class: Optional[str] = field(
            default=None,
            metadata={
                "description": "Pod QoS class. One of BestEffort, Burstable, Guaranteed."
            },
        )
        metrics_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The metric name filter consists of a regexp pattern. It specifies which metric data to return. For example, the following filter matches both pod CPU usage and memory usage: `pod_cpu_usage|pod_memory_usage`. View available metrics at [kubesphere.io](https://docs.kubesphere.io/advanced-v2.0/zh-CN/api-reference/monitoring-metrics/)."
            },
        )
        custom_filter: Optional[str] = field(
            default=None,
            metadata={"description": "The custom filter consists of PromQL queries."},
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
        sort_metric: Optional[str] = field(
            default=None,
            metadata={
                "description": "Sort pods by the specified metric. Not applicable if **start** and **end** are provided."
            },
        )
        sort_type: Optional[str] = field(
            default="desc.", metadata={"description": "Sort order. One of asc, desc."}
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
    endpoint_id: Optional[str] = field(default="handlePodMetricsQuery")
