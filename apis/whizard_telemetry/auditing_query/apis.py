from typing import Optional
from attrs import define, field
from .models import AuditingAPIResponse
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = ["QueryAuditingAPI"]


@define(kw_only=True)
@router.get("/kapis/logging.kubesphere.io/v1alpha2/auditing")
class QueryAuditingAPI(BaseAPI[AuditingAPIResponse]):
    """None"""

    @define
    class QueryParams:
        operation: Optional[str] = field(
            default="query",
            metadata={
                "description": "Operation type. This can be one of four types: query (for querying logs), statistics (for retrieving statistical data), histogram (for displaying log count by time interval) and export (for exporting logs). Defaults to query."
            },
        )
        workspace_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of workspaces. This field restricts the query to specified workspaces. For example, the following filter matches the workspace my-ws and demo-ws: `my-ws,demo-ws`."
            },
        )
        workspace_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **workspace_filter**, this field performs fuzzy matching on workspaces. For example, the following value limits the query to workspaces whose name contains the word my(My,MY,...) *OR* demo(Demo,DemO,...): `my,demo`."
            },
        )
        objectref_namespace_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of namespaces. This field restricts the query to specified `ObjectRef.Namespace`."
            },
        )
        objectref_namespace_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **objectref_namespace_filter**, this field performs fuzzy matching on `ObjectRef.Namespace`."
            },
        )
        objectref_name_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of names. This field restricts the query to specified `ObjectRef.Name`."
            },
        )
        objectref_name_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **objectref_name_filter**, this field performs fuzzy matching on `ObjectRef.Name`."
            },
        )
        level_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of levels. This know values are Metadata, Request, RequestResponse."
            },
        )
        verb_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of verbs. This field restricts the query to specified verb. This field restricts the query to specified `Verb`."
            },
        )
        user_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of user. This field restricts the query to specified user. For example, the following filter matches the user user1 and user2: `user1,user2`."
            },
        )
        user_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **user_filter**, this field performs fuzzy matching on 'User.username'. For example, the following value limits the query to user whose name contains the word my(My,MY,...) *OR* demo(Demo,DemO,...): `my,demo`."
            },
        )
        group_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. This field performs fuzzy matching on 'User.Groups'. For example, the following value limits the query to group which contains the word my(My,MY,...) *OR* demo(Demo,DemO,...): `my,demo`."
            },
        )
        source_ip_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. This field performs fuzzy matching on 'SourceIPs'. For example, the following value limits the query to SourceIPs which contains 127.0 *OR* 192.168.: `127.0,192.168.`."
            },
        )
        objectref_resource_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of resource. This field restricts the query to specified ip. This field restricts the query to specified `ObjectRef.Resource`."
            },
        )
        objectref_subresource_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of subresource. This field restricts the query to specified subresource. This field restricts the query to specified `ObjectRef.Subresource`."
            },
        )
        response_code_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of response status code. This field restricts the query to specified response status code. This field restricts the query to specified `ResponseStatus.code`."
            },
        )
        response_status_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of response status. This field restricts the query to specified response status. This field restricts the query to specified `ResponseStatus.status`."
            },
        )
        start_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query (limits `RequestReceivedTimestamp`). The format is a string representing seconds since the epoch, eg. 1136214245."
            },
        )
        end_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query (limits `RequestReceivedTimestamp`). The format is a string representing seconds since the epoch, eg. 1136214245."
            },
        )
        interval: Optional[str] = field(
            default="15m",
            metadata={
                "description": "Time interval. It requires **operation** is set to `histogram`. The format is [0-9]+[smhdwMqy]. Defaults to 15m (i.e. 15 min)."
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
        cluster: Optional[str] = field(default="host", metadata={"description": "."})

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[AuditingAPIResponse] = field(default=AuditingAPIResponse)
    endpoint_id: Optional[str] = field(default="queryAuditing")
