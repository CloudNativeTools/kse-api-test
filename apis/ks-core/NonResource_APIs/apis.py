from typing import Optional
from attrs import define, field
from .models import VersionInfo
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = ["VersionLegacyAPI", "VersionAPI"]


@define(kw_only=True)
@router.get("/kapis/version")
class VersionLegacyAPI(BaseAPI[VersionInfo]):
    """Deprecated, please use `/version` instead."""

    response: Optional[VersionInfo] = field(default=VersionInfo)
    endpoint_id: Optional[str] = field(default="version-legacy")


@define(kw_only=True)
@router.get("/version")
class VersionAPI(BaseAPI[VersionInfo]):
    """None"""

    response: Optional[VersionInfo] = field(default=VersionInfo)
    endpoint_id: Optional[str] = field(default="version")
