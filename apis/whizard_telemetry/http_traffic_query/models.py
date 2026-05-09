from __future__ import annotations

from typing import Optional, Any, List
from attrs import define, field

__ALL__ = ["EbpfResult", "EbpfAPIResponse"]


@define(kw_only=True)
class EbpfResult:
    total: int = field(metadata={"description": "total number of matched results"})
    records: Optional[List[Any]] = field(
        default=None, metadata={"description": "actual array of results"}
    )


@define(kw_only=True)
class EbpfAPIResponse:
    query: Optional[EbpfResult] = field(
        default=None, metadata={"description": "query results"}
    )
