from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict
from attrs import define, field

__ALL__ = [
    "TracingDetails",
    "TracingEdge",
    "TracingNode",
    "TracingServiceGraph",
    "TracingSpanEvent",
    "TracingSpanLink",
    "TracingInstrumentationScope",
    "TracingStatus",
    "TracingSpan",
    "TracingSpanList",
    "TracingTrace",
    "TracingTraceList",
]


@define(kw_only=True)
class TracingDetails:
    apdex: Optional[float] = field(default=None)
    apdex_threshold: Optional[float] = field(default=None)
    cluster: Optional[str] = field(default=None)
    direction: Optional[str] = field(default=None)
    failedRequestTotal: Optional[int] = field(default=None)
    failedResponseTotal: Optional[int] = field(default=None)
    messagingSystemTimeAvg: Optional[float] = field(default=None)
    namespace: Optional[str] = field(default=None)
    requestPerSec: Optional[float] = field(default=None)
    requestTimeAvg: Optional[float] = field(default=None)
    requestTotal: Optional[int] = field(default=None)
    responsePerSec: Optional[float] = field(default=None)
    responseTimeAvg: Optional[float] = field(default=None)
    responseTotal: Optional[int] = field(default=None)
    service: Optional[str] = field(default=None)


@define(kw_only=True)
class TracingEdge:
    details: TracingDetails = field()
    id: str = field()
    mainStat: str = field()
    secondaryStat: str = field()
    source: str = field()
    target: str = field()


@define(kw_only=True)
class TracingNode:
    details: TracingDetails = field()
    id: str = field()
    mainStat: str = field()
    secondaryStat: str = field()
    subTitle: str = field()
    title: str = field()


@define(kw_only=True)
class TracingServiceGraph:
    edges: List[TracingEdge] = field()
    nodes: List[TracingNode] = field()


@define(kw_only=True)
class TracingSpanEvent:
    attributes: Optional[Dict] = field(default=None)
    attributesRaw: Optional[str] = field(default=None)
    droppedAttributesCount: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None)
    timeUnixNano: Optional[int] = field(default=None)


@define(kw_only=True)
class TracingSpanLink:
    spanId: str = field()
    traceId: str = field()
    attributes: Optional[Dict] = field(default=None)
    attributesRaw: Optional[str] = field(default=None)
    droppedAttributesCount: Optional[int] = field(default=None)
    flags: Optional[int] = field(default=None)
    traceState: Optional[str] = field(default=None)


@define(kw_only=True)
class TracingInstrumentationScope:
    attributes: Optional[Dict] = field(default=None)
    attributesRaw: Optional[str] = field(default=None)
    droppedAttributesCount: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)


@define(kw_only=True)
class TracingStatus:
    code: Optional[int] = field(default=None)
    message: Optional[str] = field(default=None)


@define(kw_only=True)
class TracingSpan:
    duration: int = field()
    scope: TracingInstrumentationScope = field()
    service: str = field()
    spanId: str = field()
    status: TracingStatus = field()
    traceId: str = field()
    attributes: Optional[Dict] = field(default=None)
    attributesRaw: Optional[str] = field(default=None)
    cluster: Optional[str] = field(default=None)
    droppedAttributesCount: Optional[int] = field(default=None)
    droppedEventsCount: Optional[int] = field(default=None)
    droppedLinksCount: Optional[int] = field(default=None)
    endTime: Optional[datetime] = field(default=None)
    endTimeUnixNano: Optional[int] = field(default=None)
    events: Optional[List[TracingSpanEvent]] = field(default=None)
    flags: Optional[int] = field(default=None)
    kind: Optional[int] = field(default=None)
    links: Optional[List[TracingSpanLink]] = field(default=None)
    name: Optional[str] = field(default=None)
    namespace: Optional[str] = field(default=None)
    parentSpanId: Optional[str] = field(default=None)
    resource: Optional[Dict] = field(default=None)
    resourceRaw: Optional[str] = field(default=None)
    schemaUrl: Optional[str] = field(default=None)
    startTime: Optional[datetime] = field(default=None)
    startTimeUnixNano: Optional[int] = field(default=None)
    traceState: Optional[str] = field(default=None)


@define(kw_only=True)
class TracingSpanList:
    total: int = field()
    spans: Optional[List[TracingSpan]] = field(default=None)


@define(kw_only=True)
class TracingTrace:
    duration: int = field()
    name: str = field()
    service: str = field()
    services: List[Dict] = field()
    startTime: datetime = field()
    traceId: str = field()
    errorSpanCount: Optional[int] = field(default=None)
    spans: Optional[List[TracingSpan]] = field(default=None)


@define(kw_only=True)
class TracingTraceList:
    total: int = field()
    traces: Optional[List[TracingTrace]] = field(default=None)
