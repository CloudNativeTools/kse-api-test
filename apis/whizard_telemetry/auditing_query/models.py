from __future__ import annotations

from typing import Optional, Any, List
from attrs import define, field

__ALL__ = [
    "AuditingBucket",
    "AuditingHistogram",
    "AuditingEvents",
    "AuditingStatistics",
    "AuditingAPIResponse",
]


@define(kw_only=True)
class AuditingBucket:
    count: int = field(metadata={"description": "total number of events at intervals"})
    time: int = field(metadata={"description": "timestamp"})


@define(kw_only=True)
class AuditingHistogram:
    buckets: List[AuditingBucket] = field(
        metadata={"description": "actual array of histogram results"}
    )
    total: int = field(metadata={"description": "total number of events"})


@define(kw_only=True)
class AuditingEvents:
    records: List[Any] = field(metadata={"description": "actual array of results"})
    total: int = field(metadata={"description": "total number of matched results"})


@define(kw_only=True)
class AuditingStatistics:
    events: int = field(metadata={"description": "total number of events"})
    resources: int = field(metadata={"description": "total number of resources"})


@define(kw_only=True)
class AuditingAPIResponse:
    histogram: Optional[AuditingHistogram] = field(
        default=None, metadata={"description": "histogram results"}
    )
    query: Optional[AuditingEvents] = field(
        default=None, metadata={"description": "query results"}
    )
    statistics: Optional[AuditingStatistics] = field(
        default=None, metadata={"description": "statistics results"}
    )
