from __future__ import annotations

from typing import Optional, List
from attrs import define, field

__ALL__ = [
    "LoggingBucket",
    "LoggingHistogram",
    "LoggingRecord",
    "LoggingLogs",
    "LoggingStatistics",
    "LoggingAPIResponse",
]


@define(kw_only=True)
class LoggingBucket:
    count: int = field(metadata={"description": "total number of logs at intervals"})
    time: int = field(metadata={"description": "timestamp"})


@define(kw_only=True)
class LoggingHistogram:
    histograms: List[LoggingBucket] = field(
        metadata={"description": "actual array of histogram results"}
    )
    total: int = field(metadata={"description": "total number of logs"})


@define(kw_only=True)
class LoggingRecord:
    container: Optional[str] = field(
        default=None, metadata={"description": "container name"}
    )
    log: Optional[str] = field(default=None, metadata={"description": "log message"})
    namespace: Optional[str] = field(
        default=None, metadata={"description": "namespace"}
    )
    pod: Optional[str] = field(default=None, metadata={"description": "pod name"})
    time: Optional[str] = field(default=None, metadata={"description": "log timestamp"})


@define(kw_only=True)
class LoggingLogs:
    total: int = field(metadata={"description": "total number of matched results"})
    records: Optional[List[LoggingRecord]] = field(
        default=None, metadata={"description": "actual array of results"}
    )


@define(kw_only=True)
class LoggingStatistics:
    containers: int = field(metadata={"description": "total number of containers"})
    logs: int = field(metadata={"description": "total number of logs"})


@define(kw_only=True)
class LoggingAPIResponse:
    histogram: Optional[LoggingHistogram] = field(
        default=None, metadata={"description": "histogram results"}
    )
    query: Optional[LoggingLogs] = field(
        default=None, metadata={"description": "query results"}
    )
    statistics: Optional[LoggingStatistics] = field(
        default=None, metadata={"description": "statistics results"}
    )
