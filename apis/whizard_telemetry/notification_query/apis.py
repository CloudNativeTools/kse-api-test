from typing import Optional
from attrs import define, field
from .models import NotificationAPIResponse
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = ["SearchNotificationAPI"]


@define(kw_only=True)
@router.get("/kapis/notification.kubesphere.io/v2beta2/notifications/search")
class SearchNotificationAPI(BaseAPI[NotificationAPIResponse]):
    """None"""

    @define
    class QueryParams:
        operation: Optional[str] = field(
            default="query",
            metadata={
                "description": "Operation type. This can be one of these types: query (for querying logs) and export (for exporting logs). Defaults to query."
            },
        )
        status: Optional[str] = field(
            default=None,
            metadata={
                "description": "A comma-separated list of alert status, known values are firing and resolved."
            },
        )
        alertname: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of alert name."},
        )
        alertname_fuzzy: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of fuzzy alert name."},
        )
        alerttype: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of alert type."},
        )
        alerttype_fuzzy: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of fuzzy alert type."},
        )
        severity: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of severity."},
        )
        severity_fuzzy: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of fuzzy severity."},
        )
        namespace: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of namespaces."},
        )
        namespace_fuzzy: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of fuzzy namespaces."},
        )
        service: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of service name."},
        )
        service_fuzzy: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of fuzzy service name."},
        )
        pod: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of pod name."},
        )
        pod_fuzzy: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of fuzzy pod name."},
        )
        container: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of container name."},
        )
        container_fuzzy: Optional[str] = field(
            default=None,
            metadata={"description": "A comma-separated list of fuzzy container name."},
        )
        message_fuzzy: Optional[str] = field(
            default=None, metadata={"description": "Alert message."}
        )
        start_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query (limits `NotificationTime`). The format is a string representing seconds since the epoch, eg. 1136214245."
            },
        )
        end_time: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query (limits `NotificationTime`). The format is a string representing seconds since the epoch, eg. 1136214245."
            },
        )
        sort: Optional[str] = field(
            default=None, metadata={"description": "Sort field."}
        )
        order: Optional[str] = field(
            default="desc", metadata={"description": "Sort order. One of asc, desc."}
        )
        from_: Optional[int] = field(
            default=0,
            metadata={
                "description": "The offset from the result set. This field returns query results from the specified offset.",
                "original_name": "from",
            },
        )
        size: Optional[int] = field(
            default=10,
            metadata={
                "description": "Size of result set to return. Defaults to 10 (i.e. 10 event records)."
            },
        )
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[NotificationAPIResponse] = field(default=NotificationAPIResponse)
    endpoint_id: Optional[str] = field(default="SearchNotification")
