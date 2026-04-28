from __future__ import annotations

from typing import Optional, Dict, List, Any
from attrs import define, field

__ALL__ = [
    "ApiWorkloads",
    "V1ResourceQuotaStatus",
    "ApiResourceQuota",
    "ApiListResult",
    "OverviewMetricValue",
    "OverviewMetricData",
    "OverviewMetric",
    "OverviewMetricResults",
]


@define(kw_only=True)
class ApiWorkloads:
    data: Dict = field(metadata={"description": "the number of unhealthy workloads"})
    namespace: str = field(metadata={"description": "the name of the namespace"})
    items: Optional[Dict] = field(
        default=None, metadata={"description": "unhealthy workloads"}
    )


@define(kw_only=True)
class V1ResourceQuotaStatus:
    hard: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Hard is the set of enforced hard limits for each named resource. More info: https://kubernetes.io/docs/concepts/policy/resource-quotas/"
        },
    )
    used: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Used is the current observed total usage of the resource in the namespace."
        },
    )


@define(kw_only=True)
class ApiResourceQuota:
    data: V1ResourceQuotaStatus = field(
        metadata={"description": "resource quota status"}
    )
    namespace: str = field(metadata={"description": "namespace"})


@define(kw_only=True)
class ApiListResult:
    items: List[Any] = field()
    totalItems: int = field()


@define(kw_only=True)
class OverviewMetricValue:
    value: List[Any] = field()


@define(kw_only=True)
class OverviewMetricData:
    result: List[OverviewMetricValue] = field()
    resultType: str = field()


@define(kw_only=True)
class OverviewMetric:
    data: OverviewMetricData = field()
    metric_name: str = field()


@define(kw_only=True)
class OverviewMetricResults:
    results: List[OverviewMetric] = field()
