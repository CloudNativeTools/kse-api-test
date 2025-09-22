from typing import Optional, List
from attrs import define, field
from .models import V1alpha2HealthStatus, V1alpha2ComponentStatus
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "GetSystemHealthStatusV1alpha2API",
    "GetComponentsV1alpha2API",
    "GetComponentsStatusV1alpha2API",
    "GetSystemHealthStatusV1alpha3API",
    "GetComponentsV1alpha3API",
    "GetComponentsStatusV1alpha3API",
]


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha2/componenthealth")
class GetSystemHealthStatusV1alpha2API(BaseAPI[V1alpha2HealthStatus]):
    """None"""

    response: Optional[V1alpha2HealthStatus] = field(default=V1alpha2HealthStatus)
    endpoint_id: Optional[str] = field(default="get-system-health-status-v1alpha2")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha2/components")
class GetComponentsV1alpha2API(BaseAPI[V1alpha2ComponentStatus]):
    """None"""

    response: Optional[V1alpha2ComponentStatus] = field(default=V1alpha2ComponentStatus)
    endpoint_id: Optional[str] = field(default="get-components-v1alpha2")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha2/components/{component}")
class GetComponentsStatusV1alpha2API(BaseAPI[V1alpha2ComponentStatus]):
    """None"""

    @define
    class PathParams:
        component: str = field(metadata={"description": "component name"})

    path_params: PathParams
    response: Optional[V1alpha2ComponentStatus] = field(default=V1alpha2ComponentStatus)
    endpoint_id: Optional[str] = field(default="get-components-status-v1alpha2")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha3/componenthealth")
class GetSystemHealthStatusV1alpha3API(BaseAPI[V1alpha2HealthStatus]):
    """None"""

    response: Optional[V1alpha2HealthStatus] = field(default=V1alpha2HealthStatus)
    endpoint_id: Optional[str] = field(default="get-system-health-status-v1alpha3")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha3/components")
class GetComponentsV1alpha3API(BaseAPI[V1alpha2ComponentStatus]):
    """None"""

    response: Optional[V1alpha2ComponentStatus] = field(default=V1alpha2ComponentStatus)
    endpoint_id: Optional[str] = field(default="get-components-v1alpha3")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha3/components/{component}")
class GetComponentsStatusV1alpha3API(BaseAPI[V1alpha2ComponentStatus]):
    """None"""

    @define
    class PathParams:
        component: str = field(metadata={"description": "component name"})

    path_params: PathParams
    response: Optional[V1alpha2ComponentStatus] = field(default=V1alpha2ComponentStatus)
    endpoint_id: Optional[str] = field(default="get-components-status-v1alpha3")
