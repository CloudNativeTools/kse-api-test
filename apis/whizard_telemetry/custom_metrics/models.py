from __future__ import annotations

from typing import Optional, List, Dict
from attrs import define, field

__ALL__ = [
    "MonitoringMetricLabelSet",
    "MonitoringMetricLabelValue",
    "MonitoringMetadata",
    "MonitoringMetricValue",
    "MonitoringMetricData",
    "MonitoringMetric",
    "MonitoringValidationResult",
]


@define(kw_only=True)
class MonitoringMetricLabelSet:
    data: List[Dict] = field(metadata={"description": "actual array of results"})


@define(kw_only=True)
class MonitoringMetricLabelValue:
    data: List[str] = field()


@define(kw_only=True)
class MonitoringMetadata:
    data: List[MonitoringMetadata] = field(
        metadata={"description": "actual array of results"}
    )


@define(kw_only=True)
class MonitoringMetricValue:
    avg_value: str = field(
        metadata={"description": "average value from monitor points"}
    )
    currency_unit: str = field()
    fee: str = field(metadata={"description": "resource fee"})
    max_value: str = field(
        metadata={"description": "maximum value from monitor points"}
    )
    min_value: str = field(
        metadata={"description": "minimum value from monitor points"}
    )
    resource_unit: str = field()
    sum_value: str = field(metadata={"description": "sum value from monitor points"})
    exported_value: Optional[List[float]] = field(
        default=None,
        metadata={"description": "exported time series, values of vector type"},
    )
    exported_values: Optional[List[List[float]]] = field(
        default=None,
        metadata={"description": "exported time series, values of matrix type"},
    )
    metric: Optional[Dict] = field(
        default=None, metadata={"description": "time series labels"}
    )
    value: Optional[List[float]] = field(
        default=None, metadata={"description": "time series, values of vector type"}
    )
    values: Optional[List[List[float]]] = field(
        default=None, metadata={"description": "time series, values of matrix type"}
    )


@define(kw_only=True)
class MonitoringMetricData:
    result: Optional[List[MonitoringMetricValue]] = field(
        default=None,
        metadata={
            "description": "metric data including labels, time series and values"
        },
    )
    resultType: Optional[str] = field(
        default=None, metadata={"description": "result type, one of matrix, vector"}
    )


@define(kw_only=True)
class MonitoringMetric:
    data: Optional[MonitoringMetricData] = field(
        default=None, metadata={"description": "actual metric result"}
    )
    error: Optional[str] = field(default=None)
    metric_name: Optional[str] = field(
        default=None, metadata={"description": "metric name, eg. scheduler_up_sum"}
    )


@define(kw_only=True)
class MonitoringValidationResult:
    error: str = field()
    valid: bool = field(metadata={"description": "whether the expression is valid"})
