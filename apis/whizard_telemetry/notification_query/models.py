from __future__ import annotations

from typing import List, Any
from attrs import define, field

__ALL__ = ["NotificationNotifications", "NotificationAPIResponse"]


@define(kw_only=True)
class NotificationNotifications:
    items: List[Any] = field(metadata={"description": "actual array of results"})
    total: int = field(metadata={"description": "total number of matched results"})


@define(kw_only=True)
class NotificationAPIResponse:
    Notifications: NotificationNotifications = field(
        metadata={"description": "query results"}
    )
