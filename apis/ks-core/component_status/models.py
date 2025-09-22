from __future__ import annotations

from datetime import datetime
from typing import List, Any
from attrs import define, field

__ALL__ = ["V1alpha2ComponentStatus", "V1alpha2NodeStatus", "V1alpha2HealthStatus"]


@define(kw_only=True)
class V1alpha2ComponentStatus:
    healthyBackends: int = field(
        metadata={"description": "the number of healthy backend components"}
    )
    label: Any = field(metadata={"description": "labels"})
    name: str = field(metadata={"description": "component name"})
    namespace: str = field(metadata={"description": "the name of the namespace"})
    selfLink: str = field(metadata={"description": "self link"})
    startedAt: datetime = field(metadata={"description": "started time"})
    totalBackends: int = field(
        metadata={"description": "the total replicas of each backend system component"}
    )


@define(kw_only=True)
class V1alpha2NodeStatus:
    healthyNodes: int = field(metadata={"description": "the number of healthy nodes"})
    totalNodes: int = field(metadata={"description": "total number of nodes"})


@define(kw_only=True)
class V1alpha2HealthStatus:
    kubesphereStatus: List[V1alpha2ComponentStatus] = field(
        metadata={"description": "kubesphere components status"}
    )
    nodeStatus: V1alpha2NodeStatus = field(metadata={"description": "nodes status"})
