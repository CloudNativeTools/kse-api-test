from typing import Optional
from attrs import define, field
from .models import ApiWorkloads, ApiResourceQuota, ApiListResult, OverviewMetricResults
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "GetClusterAbnormalWorkloadsAPI",
    "GetClusterQuotasAPI",
    "ListClusterResourcesAPI",
    "GetClusterResourceAPI",
    "GetClusterOverviewAPI",
]


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha2/abnormalworkloads")
class GetClusterAbnormalWorkloadsAPI(BaseAPI[ApiWorkloads]):
    """None"""

    response: Optional[ApiWorkloads] = field(default=ApiWorkloads)
    endpoint_id: Optional[str] = field(default="get-cluster-abnormal-workloads")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha2/quotas")
class GetClusterQuotasAPI(BaseAPI[ApiResourceQuota]):
    """None"""

    response: Optional[ApiResourceQuota] = field(default=ApiResourceQuota)
    endpoint_id: Optional[str] = field(default="GetClusterQuotas")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha3/{resources}")
class ListClusterResourcesAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        resources: str = field(
            metadata={
                "description": "cluster level resource type, e.g. pods,jobs,configmaps,services."
            }
        )

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="page=1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="ascending=false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="list-cluster-resources")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha3/{resources}/{name}")
class GetClusterResourceAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        resources: str = field(
            metadata={
                "description": "cluster level resource type, e.g. pods,jobs,configmaps,services."
            }
        )
        name: str = field(
            metadata={"description": "the name of the clustered resources"}
        )

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="get-cluster-resource")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha3/metrics")
class GetClusterOverviewAPI(BaseAPI[OverviewMetricResults]):
    """None"""

    response: Optional[OverviewMetricResults] = field(default=OverviewMetricResults)
    endpoint_id: Optional[str] = field(default="GetClusterOverview")
