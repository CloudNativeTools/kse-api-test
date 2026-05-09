from typing import Optional
from attrs import define, field
from .models import MonitoringMetrics
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = ["HandleComponentMetricsQueryAPI"]


@define(kw_only=True)
@router.get("/kapis/monitoring.kubesphere.io/v1beta1/component_metrics")
class HandleComponentMetricsQueryAPI(BaseAPI[MonitoringMetrics]):
    """None"""

    @define
    class QueryParams:
        component: str = field(
            metadata={
                "description": "system component to monitor. One of etcd, apiserver, scheduler."
            }
        )
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        metrics_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "The metric name filter consists of a regexp pattern. It specifies which metric data to return. For example, the following filter matches both etcd server list and total size of the underlying database: `etcd_server_list|etcd_mvcc_db_size`. View available metrics at [kubesphere.io](https://docs.kubesphere.io/advanced-v2.0/zh-CN/api-reference/monitoring-metrics/)."
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

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[MonitoringMetrics] = field(default=MonitoringMetrics)
    endpoint_id: Optional[str] = field(default="handleComponentMetricsQuery")
