from typing import Optional
from attrs import define, field
from .models import (
    ClusterClusterStatus,
    InstanceInstanceList,
    InstanceInstance,
    V1alpha1QuotaResponseList,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "GetClusterStatusAPI",
    "ListAPI",
    "CreateAPI",
    "DeleteAPI",
    "GetAPI",
    "ListQuotasAPI",
]


@define(kw_only=True)
@router.get("/kapis/license.kubesphere.io/v1alpha1/clusterstatus")
class GetClusterStatusAPI(BaseAPI[ClusterClusterStatus]):
    """None"""

    response: Optional[ClusterClusterStatus] = field(default=ClusterClusterStatus)
    endpoint_id: Optional[str] = field(default="GetClusterStatus")


@define(kw_only=True)
@router.get("/kapis/license.kubesphere.io/v1alpha1/licenses")
class ListAPI(BaseAPI[InstanceInstanceList]):
    """None"""

    @define
    class QueryParams:
        state: Optional[str] = field(
            default=None, metadata={"description": "state of the license"}
        )
        page: Optional[str] = field(default="page=1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. sortBy=createTime"},
        )
        ascending: Optional[str] = field(
            default="ascending=false",
            metadata={"description": "sort parameters, e.g. ascending=false"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[InstanceInstanceList] = field(default=InstanceInstanceList)
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

    @define
    class RequestBodyModel:
        raw: str = field()

    request_body: RequestBodyModel

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
class GetAPI(BaseAPI[InstanceInstance]):
    """None"""

    @define
    class PathParams:
        license: str = field(metadata={"description": "specify extension name"})

    path_params: PathParams
    response: Optional[InstanceInstance] = field(default=InstanceInstance)
    endpoint_id: Optional[str] = field(default="Get")


@define(kw_only=True)
@router.get("/kapis/license.kubesphere.io/v1alpha1/quotas")
class ListQuotasAPI(BaseAPI[V1alpha1QuotaResponseList]):
    """None"""

    @define
    class QueryParams:
        scope: Optional[str] = field(
            default=None, metadata={"description": "scope of the quotas"}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "namespace of the quotas"}
        )
        workspace: Optional[str] = field(
            default=None, metadata={"description": "workspace of the quotas"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[V1alpha1QuotaResponseList] = field(
        default=V1alpha1QuotaResponseList
    )
    endpoint_id: Optional[str] = field(default="ListQuotas")
