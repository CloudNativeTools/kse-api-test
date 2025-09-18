from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from attrs import define, field

__ALL__ = [
    "Ks4ResourceStatistics",
    "LicenseClusterStatus",
    "LicenseProfile",
    "LicenseViolation",
    "LicenseInstance",
    "LicenseInstanceList",
]


@define(kw_only=True)
class Ks4ResourceStatistics:
    clusterNum: Optional[int] = field(default=None)
    cpuNum: Optional[int] = field(default=None)
    vcpuNum: Optional[int] = field(default=None)


@define(kw_only=True)
class LicenseClusterStatus:
    clusterId: str = field()
    clusterNum: int = field()
    lastUpdatedAt: datetime = field()
    hostClusterStatus: Optional[Ks4ResourceStatistics] = field(default=None)
    managedClusterStatus: Optional[Ks4ResourceStatistics] = field(default=None)
    memberClusterStatus: Optional[Ks4ResourceStatistics] = field(default=None)


@define(kw_only=True)
class LicenseProfile:
    licenseType: str = field()
    resourceType: str = field()
    corporation: Optional[str] = field(default=None)
    importedAt: Optional[datetime] = field(default=None)
    importedBy: Optional[str] = field(default=None)
    issuedAt: Optional[datetime] = field(default=None)
    notAfter: Optional[datetime] = field(default=None)
    notBefore: Optional[datetime] = field(default=None)


@define(kw_only=True)
class LicenseViolation:
    type: str = field()
    updatedAt: datetime = field()
    current: Optional[int] = field(default=None)
    expected: Optional[int] = field(default=None)
    reason: Optional[str] = field(default=None)


@define(kw_only=True)
class LicenseInstance:
    extension: str = field()
    id: str = field()
    profile: Optional[LicenseProfile] = field(default=None)
    violation: Optional[LicenseViolation] = field(default=None)


@define(kw_only=True)
class LicenseInstanceList:
    items: List[LicenseInstance] = field()
    total: int = field()
