from typing import Optional, List
from attrs import define, field
from .models import (
    V1ObjectMeta,
    V1alpha1ClusterStatus,
    V1alpha1ClusterSpec,
    V1alpha1BindingClustersRequest,
    ApiListResult,
    V1alpha1CreateLabelRequest,
    V1alpha1Label,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "UpdateKubeConfigAPI",
    "ValidateClusterAPI",
    "BindingClustersAPI",
    "DeleteLabelsAPI",
    "ListLabelGroupsAPI",
    "CreateLabelsAPI",
    "UpdateLabelAPI",
]


@define(kw_only=True)
@router.put("/kapis/cluster.kubesphere.io/v1alpha1/clusters/{cluster}/kubeconfig")
class UpdateKubeConfigAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="updateKubeConfig")


@define(kw_only=True)
@router.post("/kapis/cluster.kubesphere.io/v1alpha1/clusters/validation")
class ValidateClusterAPI(BaseAPI):
    """None"""

    @define
    class RequestBodyModel:
        apiVersion: Optional[str] = field(
            default=None,
            metadata={
                "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
            },
        )
        kind: Optional[str] = field(
            default=None,
            metadata={
                "description": "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
            },
        )
        metadata: Optional[V1ObjectMeta] = field(default=None)
        spec: Optional[V1alpha1ClusterSpec] = field(default=None)
        status: Optional[V1alpha1ClusterStatus] = field(default=None)

    request_body: RequestBodyModel

    endpoint_id: Optional[str] = field(default="validateCluster")


@define(kw_only=True)
@router.post("/kapis/cluster.kubesphere.io/v1alpha1/labelbindings")
class BindingClustersAPI(BaseAPI):
    """None"""

    request_body: List[V1alpha1BindingClustersRequest] = field()

    endpoint_id: Optional[str] = field(default="bindingClusters")


@define(kw_only=True)
@router.delete("/kapis/cluster.kubesphere.io/v1alpha1/labels")
class DeleteLabelsAPI(BaseAPI):
    """None"""

    request_body: List[str] = field()

    endpoint_id: Optional[str] = field(default="deleteLabels")


@define(kw_only=True)
@router.get("/kapis/cluster.kubesphere.io/v1alpha1/labels")
class ListLabelGroupsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="listLabelGroups")


@define(kw_only=True)
@router.post("/kapis/cluster.kubesphere.io/v1alpha1/labels")
class CreateLabelsAPI(BaseAPI[ApiListResult]):
    """None"""

    request_body: List[V1alpha1CreateLabelRequest] = field()

    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="createLabels")


@define(kw_only=True)
@router.put("/kapis/cluster.kubesphere.io/v1alpha1/labels/{label}")
class UpdateLabelAPI(BaseAPI[V1alpha1Label]):
    """None"""

    @define
    class PathParams:
        label: str = field(metadata={"description": "Name of the label."})

    @define
    class RequestBodyModel:
        key: str = field()
        value: str = field()

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1alpha1Label] = field(default=V1alpha1Label)
    endpoint_id: Optional[str] = field(default="updateLabel")
