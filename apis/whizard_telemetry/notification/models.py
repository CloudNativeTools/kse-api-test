from __future__ import annotations

from typing import Any, List
from attrs import define, field

__ALL__ = ["ApiListResult", "ErrorsError"]


@define(kw_only=True)
class ApiListResult:
    items: List[Any] = field()
    totalItems: int = field()


@define(kw_only=True)
class ErrorsError:
    message: str = field(metadata={"description": "error message"})
