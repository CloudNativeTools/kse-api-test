from typing import Optional
from attrs import define, field
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "HandleProxyAPI",
    "HandleProxyAPI_1",
    "HandleProxyAPI_2",
    "HandleProxyAPI_3",
    "HandleProxyAPI_4",
    "HandleProxyAPI_5",
    "HandleProxyAPI_6",
    "Func1API",
]


@define(kw_only=True)
@router.get("/kapis/monitoring.observability.kubesphere.io/v1alpha1/configs/global")
class HandleProxyAPI(BaseAPI):
    endpoint_id: Optional[str] = field(default="handleProxy")


@define(kw_only=True)
@router.put("/kapis/monitoring.observability.kubesphere.io/v1alpha1/configs/global")
class HandleProxyAPI_1(BaseAPI):
    endpoint_id: Optional[str] = field(default="handleProxy")


@define(kw_only=True)
@router.post("/kapis/monitoring.observability.kubesphere.io/v1alpha1/configs/storage")
class HandleProxyAPI_2(BaseAPI):
    endpoint_id: Optional[str] = field(default="handleProxy")


@define(kw_only=True)
@router.get(
    "/kapis/monitoring.observability.kubesphere.io/v1alpha1/configs/storage/{default}"
)
class HandleProxyAPI_3(BaseAPI):
    endpoint_id: Optional[str] = field(default="handleProxy")


@define(kw_only=True)
@router.put(
    "/kapis/monitoring.observability.kubesphere.io/v1alpha1/configs/storage/{default}"
)
class HandleProxyAPI_4(BaseAPI):
    endpoint_id: Optional[str] = field(default="handleProxy")


@define(kw_only=True)
@router.delete(
    "/kapis/monitoring.observability.kubesphere.io/v1alpha1/configs/storage/{default}"
)
class HandleProxyAPI_5(BaseAPI):
    endpoint_id: Optional[str] = field(default="handleProxy")


@define(kw_only=True)
@router.post(
    "/kapis/monitoring.observability.kubesphere.io/v1alpha1/configs/storage/{default}/verify"
)
class HandleProxyAPI_6(BaseAPI):
    endpoint_id: Optional[str] = field(default="handleProxy")


@define(kw_only=True)
@router.get("/kapis/version")
class Func1API(BaseAPI):
    endpoint_id: Optional[str] = field(default="func1")