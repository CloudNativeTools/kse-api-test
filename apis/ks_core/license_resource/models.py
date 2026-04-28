from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Any, Dict
from attrs import define, field

__ALL__ = [
    "ClusterClusterStatus",
    "TypesPlan",
    "TypesLicenseMetaData",
    "TypesFeatureGates",
    "TypesUser",
    "TypesResourceLimit",
    "InstanceProfile",
    "BigInt",
    "InfDec",
    "ResourceInfDecAmount",
    "ResourceInt64Amount",
    "ResourceQuantity",
    "InstanceViolation",
    "InstanceInstance",
    "InstanceInstanceList",
    "V1alpha1QuotaResponse",
    "V1alpha1QuotaResponseList",
]


@define(kw_only=True)
class ClusterClusterStatus:
    clusterId: str = field()


@define(kw_only=True)
class TypesPlan:
    displayName: Optional[Dict] = field(default=None)
    name: Optional[str] = field(default=None)


@define(kw_only=True)
class TypesLicenseMetaData:
    customParameters: Optional[Dict] = field(default=None)
    plan: Optional[TypesPlan] = field(default=None)
    signature: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)


@define(kw_only=True)
class TypesFeatureGates:
    cluster: Optional[Dict] = field(default=None)
    global_: Optional[Dict] = field(default=None, metadata={"original_name": "global"})
    namespace: Optional[Dict] = field(default=None)
    workspace: Optional[Dict] = field(default=None)


@define(kw_only=True)
class TypesUser:
    co: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)


@define(kw_only=True)
class TypesResourceLimit:
    cluster: Optional[Dict] = field(default=None)
    global_: Optional[Dict] = field(default=None, metadata={"original_name": "global"})
    namespace: Optional[Dict] = field(default=None)
    workspace: Optional[Dict] = field(default=None)


@define(kw_only=True)
class InstanceProfile:
    componentName: str = field()
    id: str = field()
    licenseType: str = field()
    clusterId: Optional[str] = field(default=None)
    corporation: Optional[str] = field(default=None)
    customParameters: Optional[str] = field(default=None)
    featureGates: Optional[TypesFeatureGates] = field(default=None)
    importedAt: Optional[datetime] = field(default=None)
    importedBy: Optional[str] = field(default=None)
    issueAt: Optional[datetime] = field(default=None)
    issuer: Optional[TypesUser] = field(default=None)
    notAfter: Optional[datetime] = field(default=None)
    notBefore: Optional[datetime] = field(default=None)
    resourceLimit: Optional[TypesResourceLimit] = field(default=None)
    subject: Optional[TypesUser] = field(default=None)


@define(kw_only=True)
class BigInt:
    abs: Any = field()
    neg: Any = field()


@define(kw_only=True)
class InfDec:
    scale: int = field()
    unscaled: BigInt = field()


@define(kw_only=True)
class ResourceInfDecAmount:
    Dec: InfDec = field()


@define(kw_only=True)
class ResourceInt64Amount:
    scale: int = field()
    value: int = field()


@define(kw_only=True)
class ResourceQuantity:
    Format: str = field()
    d: ResourceInfDecAmount = field()
    i: ResourceInt64Amount = field()
    s: str = field()


@define(kw_only=True)
class InstanceViolation:
    type: str = field()
    updatedAt: datetime = field()
    current: Optional[ResourceQuantity] = field(default=None)
    expected: Optional[ResourceQuantity] = field(default=None)
    reason: Optional[str] = field(default=None)


@define(kw_only=True)
class InstanceInstance:
    extension: str = field()
    cloudUserID: Optional[str] = field(default=None)
    maintenance: Optional[str] = field(default=None)
    metadata: Optional[TypesLicenseMetaData] = field(default=None)
    profile: Optional[InstanceProfile] = field(default=None)
    state: Optional[str] = field(default=None)
    violation: Optional[InstanceViolation] = field(default=None)


@define(kw_only=True)
class InstanceInstanceList:
    items: List[InstanceInstance] = field()
    total: int = field()


@define(kw_only=True)
class V1alpha1QuotaResponse:
    extension: str = field()
    limit: ResourceQuantity = field()
    name: str = field()
    value: ResourceQuantity = field()


@define(kw_only=True)
class V1alpha1QuotaResponseList:
    items: List[V1alpha1QuotaResponse] = field()
    total: int = field()
