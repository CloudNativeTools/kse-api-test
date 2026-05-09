from typing import List, Optional, Any
from attrs import define, field
from .models import TracingServiceGraph, TracingSpanList, TracingTraceList
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "GetApdexThresholdAPI",
    "SetApdexThresholdAPI",
    "GetHistogramAPI",
    "GetServiceGraphAPI",
    "GetServicesAPI",
    "GetSpansAPI",
    "GetTagsAPI",
    "GetTracesAPI",
    "GetValuesByTagAPI",
    "GetAssociatedWorkloadAPI",
]


@define(kw_only=True)
@router.get("/kapis/tracing.wiztelemetry.io/v1alpha1/apdex/thresholds")
class GetApdexThresholdAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        keys: List[str] = field(metadata={"description": "The keys of links."})

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="GetApdexThreshold")


@define(kw_only=True)
@router.put("/kapis/tracing.wiztelemetry.io/v1alpha1/apdex/thresholds")
class SetApdexThresholdAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="SetApdexThreshold")


@define(kw_only=True)
@router.get("/kapis/tracing.wiztelemetry.io/v1alpha1/histogram")
class GetHistogramAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        key: Optional[str] = field(
            default=None, metadata={"description": "The key of node of edge."}
        )
        kind: Optional[str] = field(
            default=None,
            metadata={
                "description": "The histogram kind, known values are, RequestTotal: 1, RequestTimeAverage: 2, FailedRequestTotal: 3, ResponseTotal: 4, ResponseTimeAverage:5, FailedResponseTotal:6"
            },
        )
        interval: Optional[str] = field(
            default=None,
            metadata={
                "description": "Time interval. The format is [0-9]+[smhdwMqy]. Defaults to 15m (i.e. 15 min)."
            },
        )
        startTime: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query. Default to 0. The format is a string representing seconds since the epoch, eg. 1559664000."
            },
        )
        endTime: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query. Default to now. The format is a string representing seconds since the epoch, eg. 1559664000."
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="GetHistogram")


@define(kw_only=True)
@router.post("/kapis/tracing.wiztelemetry.io/v1alpha1/servicegraphs")
class GetServiceGraphAPI(BaseAPI[TracingServiceGraph]):
    """None"""

    response: Optional[TracingServiceGraph] = field(default=TracingServiceGraph)
    endpoint_id: Optional[str] = field(default="GetServiceGraph")


@define(kw_only=True)
@router.get("/kapis/tracing.wiztelemetry.io/v1alpha1/services")
class GetServicesAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="GetServices")


@define(kw_only=True)
@router.post("/kapis/tracing.wiztelemetry.io/v1alpha1/spans")
class GetSpansAPI(BaseAPI[TracingSpanList]):
    """None"""

    response: Optional[TracingSpanList] = field(default=TracingSpanList)
    endpoint_id: Optional[str] = field(default="GetSpans")


@define(kw_only=True)
@router.get("/kapis/tracing.wiztelemetry.io/v1alpha1/tags")
class GetTagsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="GetTags")


@define(kw_only=True)
@router.post("/kapis/tracing.wiztelemetry.io/v1alpha1/traces")
class GetTracesAPI(BaseAPI[TracingTraceList]):
    """None"""

    response: Optional[TracingTraceList] = field(default=TracingTraceList)
    endpoint_id: Optional[str] = field(default="GetTraces")


@define(kw_only=True)
@router.get("/kapis/tracing.wiztelemetry.io/v1alpha1/values")
class GetValuesByTagAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        tags: Optional[str] = field(
            default=None, metadata={"description": "A comma-separated list of tag."}
        )
        limit: Optional[Any] = field(
            default=None,
            metadata={"description": "The maximum number of values for each tag."},
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="GetValuesByTag")


@define(kw_only=True)
@router.get("/kapis/tracing.wiztelemetry.io/v1alpha1/workloads")
class GetAssociatedWorkloadAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        keys: Optional[List[str]] = field(
            default=None, metadata={"description": "The keys of node."}
        )
        startTime: Optional[str] = field(
            default=None,
            metadata={
                "description": "Start time of query. Default to 0. The format is a string representing seconds since the epoch, eg. 1559664000."
            },
        )
        endTime: Optional[str] = field(
            default=None,
            metadata={
                "description": "End time of query. Default to now. The format is a string representing seconds since the epoch, eg. 1559664000."
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="GetAssociatedWorkload")
