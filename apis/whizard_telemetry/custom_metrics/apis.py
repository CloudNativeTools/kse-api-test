from typing import Optional, List
from attrs import define, field
from .models import (
    MonitoringMetricLabelSet,
    MonitoringMetricLabelValue,
    MonitoringMetadata,
    MonitoringMetric,
    MonitoringValidationResult,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "HandleMetricLabelSetQueryAPI",
    "HandleLabelValuesQueryAPI",
    "HandleMetadataQueryAPI",
    "HandleAdhocQueryAPI",
    "HandleValidateQueryExpressionAPI",
]


@define(kw_only=True)
@router.get("/kapis/monitoring.kubesphere.io/v1beta1/targets/labelsets")
class HandleMetricLabelSetQueryAPI(BaseAPI[MonitoringMetricLabelSet]):
    """None"""

    @define
    class QueryParams:
        metric: str = field(metadata={"description": "The name of the metric"})
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
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

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[MonitoringMetricLabelSet] = field(
        default=MonitoringMetricLabelSet
    )
    endpoint_id: Optional[str] = field(default="handleMetricLabelSetQuery")


@define(kw_only=True)
@router.get("/kapis/monitoring.kubesphere.io/v1beta1/targets/labelvalues")
class HandleLabelValuesQueryAPI(BaseAPI[MonitoringMetricLabelValue]):
    """None"""

    @define
    class QueryParams:
        label: str = field(metadata={"description": "The name of the metric"})
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        matches: Optional[List[str]] = field(default=None)
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

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[MonitoringMetricLabelValue] = field(
        default=MonitoringMetricLabelValue
    )
    endpoint_id: Optional[str] = field(default="handleLabelValuesQuery")


@define(kw_only=True)
@router.get("/kapis/monitoring.kubesphere.io/v1beta1/targets/metadata")
class HandleMetadataQueryAPI(BaseAPI[MonitoringMetadata]):
    """None"""

    @define
    class QueryParams:
        metric: str = field(metadata={"description": "The name of the metric"})
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[MonitoringMetadata] = field(default=MonitoringMetadata)
    endpoint_id: Optional[str] = field(default="handleMetadataQuery")


@define(kw_only=True)
@router.get("/kapis/monitoring.kubesphere.io/v1beta1/targets/query")
class HandleAdhocQueryAPI(BaseAPI[MonitoringMetric]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "Cluster name."}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "Namespace name."}
        )
        expr: Optional[str] = field(
            default=None, metadata={"description": "The expression to be evaluated."}
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
    response: Optional[MonitoringMetric] = field(default=MonitoringMetric)
    endpoint_id: Optional[str] = field(default="handleAdhocQuery")


@define(kw_only=True)
@router.get("/kapis/monitoring.kubesphere.io/v1beta1/validation/query")
class HandleValidateQueryExpressionAPI(BaseAPI[MonitoringValidationResult]):
    """None"""

    @define
    class QueryParams:
        expr: str = field(metadata={"description": "The expression to be validated."})

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[MonitoringValidationResult] = field(
        default=MonitoringValidationResult
    )
    endpoint_id: Optional[str] = field(default="handleValidateQueryExpression")
