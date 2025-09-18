from typing import Optional
from attrs import define, field
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "ComponentConfigAPI",
    "MarketplaceConfigAPI",
    "OauthConfigAPI",
    "GetThemeConfigAPI",
    "UpdateThemeConfigAPI",
]


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/configz")
class ComponentConfigAPI(BaseAPI):
    """Information about the components configuration"""

    endpoint_id: Optional[str] = field(default="component-config")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/marketplace")
class MarketplaceConfigAPI(BaseAPI):
    """Retrieve marketplace configuration."""

    endpoint_id: Optional[str] = field(default="marketplace-config")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/oauth")
class OauthConfigAPI(BaseAPI):
    """Information about the authorization server are published."""

    endpoint_id: Optional[str] = field(default="oauth-config")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/theme")
class GetThemeConfigAPI(BaseAPI):
    """Retrieve theme configuration settings."""

    endpoint_id: Optional[str] = field(default="get-theme-config")


@define(kw_only=True)
@router.post("/kapis/config.kubesphere.io/v1alpha2/configs/theme")
class UpdateThemeConfigAPI(BaseAPI):
    """Update theme configuration settings."""

    endpoint_id: Optional[str] = field(default="update-theme-config")
