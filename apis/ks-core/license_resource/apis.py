from typing import Optional, List
from attrs import define, field
from .models import LicenseClusterStatus, LicenseInstanceList, LicenseInstance
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = ["GetClusterStatusAPI", "ListAPI", "CreateAPI", "DeleteAPI", "GetAPI"]


@define(kw_only=True)
@router.get("/kapis/license.kubesphere.io/v1alpha1/clusterstatus")
class GetClusterStatusAPI(BaseAPI[LicenseClusterStatus]):
    """None"""

    response: Optional[LicenseClusterStatus] = field(default=LicenseClusterStatus)
    endpoint_id: Optional[str] = field(default="GetClusterStatus")


@define(kw_only=True)
@router.get("/kapis/license.kubesphere.io/v1alpha1/licenses")
class ListAPI(BaseAPI[LicenseInstanceList]):
    """None"""

    response: Optional[LicenseInstanceList] = field(default=LicenseInstanceList)
    endpoint_id: Optional[str] = field(default="List")


@define(kw_only=True)
@router.post("/kapis/license.kubesphere.io/v1alpha1/licenses")
class CreateAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        validate: Optional[str] = field(
            default=None, metadata={"description": "Validate license"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="Create")


@define(kw_only=True)
@router.delete("/kapis/license.kubesphere.io/v1alpha1/licenses/{license}")
class DeleteAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        license: str = field(metadata={"description": "specify the license"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="Delete")


@define(kw_only=True)
@router.get("/kapis/license.kubesphere.io/v1alpha1/licenses/{license}")
class GetAPI(BaseAPI[LicenseInstance]):
    """None"""

    @define
    class PathParams:
        license: str = field(metadata={"description": "specify extension name"})

    path_params: PathParams
    response: Optional[LicenseInstance] = field(default=LicenseInstance)
    endpoint_id: Optional[str] = field(default="Get")
