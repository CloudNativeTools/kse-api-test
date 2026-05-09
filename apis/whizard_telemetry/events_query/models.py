from __future__ import annotations

from typing import Optional, Any, List
from attrs import define, field

__ALL__ = [
    "EventsBucket",
    "EventsHistogram",
    "EventsEvents",
    "EventsStatistics",
    "EventsAPIResponse",
]


@define(kw_only=True)
class EventsBucket:
    count: int = field(metadata={"description": "total number of events at intervals"})
    time: int = field(metadata={"description": "timestamp"})


@define(kw_only=True)
class EventsHistogram:
    buckets: List[EventsBucket] = field(
        metadata={"description": "actual array of histogram results"}
    )
    total: int = field(metadata={"description": "total number of events"})


@define(kw_only=True)
class EventsEvents:
    records: List[Any] = field(metadata={"description": "actual array of results"})
    total: int = field(metadata={"description": "total number of matched results"})


@define(kw_only=True)
class EventsStatistics:
    events: int = field(metadata={"description": "total number of events"})
    resources: int = field(metadata={"description": "total number of resources"})


@define(kw_only=True)
class EventsAPIResponse:
    histogram: Optional[EventsHistogram] = field(
        default=None, metadata={"description": "histogram results"}
    )
    query: Optional[EventsEvents] = field(
        default=None, metadata={"description": "query results"}
    )
    statistics: Optional[EventsStatistics] = field(
        default=None, metadata={"description": "statistics results"}
    )
