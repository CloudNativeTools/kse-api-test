from typing import Optional
from attrs import define, field
from .models import EventsAPIResponse
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "QueryEventsAPI",
    "FieldsAPI",
    "LabelvaluesAPI",
    "NamespacesAPI",
    "PlacementAPI",
    "QueryAPI",
    "ResourcesAPI",
    "StatisticsAPI",
]


@define(kw_only=True)
@router.get("/kapis/logging.kubesphere.io/v1alpha2/events")
class QueryEventsAPI(BaseAPI[EventsAPIResponse]):
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
        involved_object_namespace_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of namespaces. This field restricts the query to specified `involvedObject.namespace`."
            },
        )
        involved_object_namespace_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **involved_object_namespace_filter**, this field performs fuzzy matching on `involvedObject.namespace`"
            },
        )
        involved_object_name_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of names. This field restricts the query to specified `involvedObject.name`."
            },
        )
        involved_object_name_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **involved_object_name_filter**, this field performs fuzzy matching on `involvedObject.name`."
            },
        )
        involved_object_kind_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of kinds. This field restricts the query to specified `involvedObject.kind`."
            },
        )
        reason_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of reasons. This field restricts the query to specified `reason`."
            },
        )
        reason_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. Differing from **reason_filter**, this field performs fuzzy matching on `reason`."
            },
        )
        message_search: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of keywords. This field performs fuzzy matching on `message`."
            },
        )
        type_filter: Optional[str] = field(
            default=None,
            metadata={
                "description": "Type of event matching on `type`. This can be one of two types: `Warning`, `Normal`"
            },
        )
        start_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query (limits `lastTimestamp`). The format is a string representing seconds since the epoch, eg. 1136214245."
            },
        )
        end_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query (limits `lastTimestamp`). The format is a string representing seconds since the epoch, eg. 1136214245."
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
                "description": "Sort order. One of asc, desc. This field sorts events by `lastTimestamp`."
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
        cluster: Optional[str] = field(
            default="host", metadata={"description": "cluster name."}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[EventsAPIResponse] = field(default=EventsAPIResponse)
    endpoint_id: Optional[str] = field(default="queryEvents")


@define(kw_only=True)
@router.get("/kapis/logging.wiztelemetry.io/v2alpha1/events/fields")
class FieldsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="fields")


@define(kw_only=True)
@router.get("/kapis/logging.wiztelemetry.io/v2alpha1/events/labelvalues")
class LabelvaluesAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(default=None)

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="labelvalues")


@define(kw_only=True)
@router.get("/kapis/logging.wiztelemetry.io/v2alpha1/events/namespaces")
class NamespacesAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        cluster: str = field()

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="namespaces")


@define(kw_only=True)
@router.get("/kapis/logging.wiztelemetry.io/v2alpha1/events/placement")
class PlacementAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="placement")


@define(kw_only=True)
@router.post("/kapis/logging.wiztelemetry.io/v2alpha1/events/query")
class QueryAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="query")


@define(kw_only=True)
@router.get("/kapis/logging.wiztelemetry.io/v2alpha1/events/resources")
class ResourcesAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        cluster: str = field()
        namespace: str = field()

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="resources")


@define(kw_only=True)
@router.post("/kapis/logging.wiztelemetry.io/v2alpha1/events/statistics")
class StatisticsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="statistics")
