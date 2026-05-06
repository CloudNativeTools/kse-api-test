from typing import Optional
from attrs import define, field
from .models import LoggingAPIResponse
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = ["QueryLogsAPI"]


@define(kw_only=True)
@router.get("/kapis/logging.kubesphere.io/v1alpha2/logs")
class QueryLogsAPI(BaseAPI[LoggingAPIResponse]):
    """None"""

    @define
    class QueryParams:
        operation: Optional[str] = field(
            default="query",
            metadata={
                "description": "Operation type. This can be one of four types: query (for querying logs), statistics (for retrieving statistical data), histogram (for displaying log count by time interval) and export (for exporting logs). Defaults to query."
            },
        )
        namespaces: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of namespaces. This field restricts the query to specified namespaces. For example, the following filter matches the namespace my-ns and demo-ns: `my-ns,demo-ns`"
            },
        )
        namespace_query: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **namespaces**, this field performs fuzzy matching on namespaces. For example, the following value limits the query to namespaces whose name contains the word my(My,MY,...) *OR* demo(Demo,DemO,...): `my,demo`."
            },
        )
        workloads: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of workloads. This field restricts the query to specified workloads. For example, the following filter matches the workload my-wl and demo-wl: `my-wl,demo-wl`"
            },
        )
        workload_query: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **workloads**, this field performs fuzzy matching on workloads. For example, the following value limits the query to workloads whose name contains the word my(My,MY,...) *OR* demo(Demo,DemO,...): `my,demo`."
            },
        )
        pods: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of pods. This field restricts the query to specified pods. For example, the following filter matches the pod my-po and demo-po: `my-po,demo-po`"
            },
        )
        pod_query: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **pods**, this field performs fuzzy matching on pods. For example, the following value limits the query to pods whose name contains the word my(My,MY,...) *OR* demo(Demo,DemO,...): `my,demo`."
            },
        )
        containers: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of containers. This field restricts the query to specified containers. For example, the following filter matches the container my-cont and demo-cont: `my-cont,demo-cont`"
            },
        )
        container_query: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **containers**, this field performs fuzzy matching on containers. For example, the following value limits the query to containers whose name contains the word my(My,MY,...) *OR* demo(Demo,DemO,...): `my,demo`."
            },
        )
        log_query: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. The query returns logs which contain at least one keyword. Case-insensitive matching. For example, if the field is set to `err,INFO`, the query returns any log containing err(ERR,Err,...) *OR* INFO(info,InFo,...)."
            },
        )
        interval: Optional[str] = field(
            default="15m",
            metadata={
                "description": "Time interval. It requires **operation** is set to histogram. The format is [0-9]+[smhdwMqy]. Defaults to 15m (i.e. 15 min)."
            },
        )
        start_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query. Default to 0. The format is a string representing seconds since the epoch, eg. 1559664000."
            },
        )
        end_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query. Default to now. The format is a string representing seconds since the epoch, eg. 1559664000."
            },
        )
        sort: Optional[str] = field(
            default="desc",
            metadata={
                "description": "Sort order. One of asc, desc. This field sorts logs by timestamp."
            },
        )
        from_: Optional[int] = field(
            default=0,
            metadata={
                "description": "The offset from the result set. This field returns query results from the specified offset. It requires **operation** is set to query. Defaults to 0 (i.e. from the beginning of the result set).",
                "original_name": "from",
            },
        )
        size: Optional[int] = field(
            default=10,
            metadata={
                "description": "Size of result to return. It requires **operation** is set to query. Defaults to 10 (i.e. 10 log records)."
            },
        )
        cluster: Optional[str] = field(
            default="host", metadata={"description": "cluster name."}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[LoggingAPIResponse] = field(default=LoggingAPIResponse)
    endpoint_id: Optional[str] = field(default="queryLogs")
