from typing import Optional
from attrs import define, field
from .models import EbpfAPIResponse
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = ["QueryTrafficAPI"]


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
