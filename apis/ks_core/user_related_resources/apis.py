from typing import Optional, List
from attrs import define, field
from .models import (
    V1beta1WorkspaceTemplate,
    V1alpha1UpdateVisibilityRequest,
    ApiListResult,
    V1alpha1Workspace,
    V1Namespace,
    V1alpha2WorkspaceTemplate,
    OverviewMetricResults,
    V1beta1WorkspaceTemplateSpec,
    V1ObjectMeta,
    ErrorsError,
    V1NamespaceSpec,
    V1NamespaceStatus,
    V1alpha2ResourceQuotaStatus,
    V1alpha2ResourceQuota,
    V1alpha2ResourceQuotaSpec,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "PatchWorkspaceTemplateClustersVisibilityAPI",
    "GetKubeconfigAPI",
    "ListClustersAPI",
    "ListNamespacesAPI",
    "ListWorkspacesAPI",
    "GetWorkspaceAPI",
    "ListWorkspaceClustersAPI",
    "ListNamespacesAPI_1",
    "DescribeNamespaceAPI",
    "ListWorkspaceTemplatesAPI",
    "DescribeWorkspaceTemplateAPI",
    "UserRelatedClustersAPI",
    "GetPlatformMetricsAPI",
    "ListNamespacesAPI_2",
    "ListWorkspacesAPI_1",
    "CreateWorkspaceAPI",
    "DeleteWorkspaceAPI",
    "GetWorkspaceAPI_1",
    "PatchWorkspaceAPI",
    "UpdateWorkspaceAPI",
    "ListWorkspaceClustersAPI_1",
    "GetWorkspaceMetricsAPI",
    "ListNamespacesWorkspaceAPI",
    "CreateNamespaceAPI",
    "DeleteNamespaceAPI",
    "DescribeNamespaceAPI_1",
    "PatchNamespaceAPI",
    "UpdateNamespaceAPI",
    "CreateWorkspaceResourceQuotaAPI",
    "DeleteWorkspaceResourceQuotaAPI",
    "DescribeWorkspaceResourceQuotaAPI",
    "UpdateWorkspaceResourceQuotaAPI",
    "ListNamespacesWorkspaceMemberAPI",
    "ListWorkspaceTemplatesAPI_1",
    "CreateWorkspaceTemplateAPI",
    "DeleteWorkspaceTemplateAPI",
    "GetWorkspaceTemplateAPI",
    "PatchWorkspaceTemplateAPI",
    "UpdateWorkspaceTemplateAPI",
]


@define(kw_only=True)
@router.post("/kapis/cluster.kubesphere.io/v1alpha1/clusters/{cluster}/grantrequests")
class PatchWorkspaceTemplateClustersVisibilityAPI(BaseAPI[V1beta1WorkspaceTemplate]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})

    request_body: List[V1alpha1UpdateVisibilityRequest] = field()

    path_params: PathParams
    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(
        default="patch-workspace-template-clusters-visibility"
    )


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha2/users/{user}/kubeconfig")
class GetKubeconfigAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "username"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="GetKubeconfig")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1alpha3/clusters")
class ListClustersAPI(BaseAPI[ApiListResult]):
    """None"""

    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListClusters")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1alpha3/namespaces")
class ListNamespacesAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListNamespaces")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1alpha3/workspaces")
class ListWorkspacesAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListWorkspaces")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1alpha3/workspaces/{workspace}")
class GetWorkspaceAPI(BaseAPI[V1alpha1Workspace]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace name"})

    path_params: PathParams
    response: Optional[V1alpha1Workspace] = field(default=V1alpha1Workspace)
    endpoint_id: Optional[str] = field(default="GetWorkspace")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1alpha3/workspaces/{workspace}/clusters")
class ListWorkspaceClustersAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace name"})

    path_params: PathParams
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListWorkspaceClusters")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1alpha3/workspaces/{workspace}/namespaces")
class ListNamespacesAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace name"})

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListNamespaces")


@define(kw_only=True)
@router.get(
    "/kapis/tenant.kubesphere.io/v1alpha3/workspaces/{workspace}/namespaces/{namespace}"
)
class DescribeNamespaceAPI(BaseAPI[V1Namespace]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace name"})
        namespace: str = field(metadata={"description": "project name"})

    path_params: PathParams
    response: Optional[V1Namespace] = field(default=V1Namespace)
    endpoint_id: Optional[str] = field(default="DescribeNamespace")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1alpha3/workspacetemplates")
class ListWorkspaceTemplatesAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListWorkspaceTemplates")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1alpha3/workspacetemplates/{workspace}")
class DescribeWorkspaceTemplateAPI(BaseAPI[V1alpha2WorkspaceTemplate]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace name"})

    path_params: PathParams
    response: Optional[V1alpha2WorkspaceTemplate] = field(
        default=V1alpha2WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="DescribeWorkspaceTemplate")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/clusters")
class UserRelatedClustersAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="user-related-clusters")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/metrics")
class GetPlatformMetricsAPI(BaseAPI[OverviewMetricResults]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[OverviewMetricResults] = field(default=OverviewMetricResults)
    endpoint_id: Optional[str] = field(default="GetPlatformMetrics")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/namespaces")
class ListNamespacesAPI_2(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="list-namespaces")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/workspaces")
class ListWorkspacesAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="list-workspaces")


@define(kw_only=True)
@router.post("/kapis/tenant.kubesphere.io/v1beta1/workspaces")
class CreateWorkspaceAPI(BaseAPI[V1beta1WorkspaceTemplate]):
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
        spec: Optional[V1beta1WorkspaceTemplateSpec] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="create-workspace")


@define(kw_only=True)
@router.delete("/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}")
class DeleteWorkspaceAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="delete-workspace")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}")
class GetWorkspaceAPI_1(BaseAPI[V1beta1WorkspaceTemplate]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    path_params: PathParams
    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="get-workspace")


@define(kw_only=True)
@router.patch("/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}")
class PatchWorkspaceAPI(BaseAPI[V1beta1WorkspaceTemplate]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

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
        spec: Optional[V1beta1WorkspaceTemplateSpec] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="patch-workspace")


@define(kw_only=True)
@router.put("/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}")
class UpdateWorkspaceAPI(BaseAPI[V1beta1WorkspaceTemplate]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

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
        spec: Optional[V1beta1WorkspaceTemplateSpec] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="update-workspace")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/clusters")
class ListWorkspaceClustersAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    path_params: PathParams
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListWorkspaceClusters")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/metrics")
class GetWorkspaceMetricsAPI(BaseAPI[OverviewMetricResults]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[OverviewMetricResults] = field(default=OverviewMetricResults)
    endpoint_id: Optional[str] = field(default="GetWorkspaceMetrics")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/namespaces")
class ListNamespacesWorkspaceAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="list-namespaces-workspace")


@define(kw_only=True)
@router.post("/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/namespaces")
class CreateNamespaceAPI(BaseAPI[V1Namespace]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

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
        metadata: Optional[V1ObjectMeta] = field(
            default=None,
            metadata={
                "description": "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
            },
        )
        spec: Optional[V1NamespaceSpec] = field(
            default=None,
            metadata={
                "description": "Spec defines the behavior of the Namespace. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
            },
        )
        status: Optional[V1NamespaceStatus] = field(
            default=None,
            metadata={
                "description": "Status describes the current status of a Namespace. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
            },
        )

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1Namespace] = field(default=V1Namespace)
    endpoint_id: Optional[str] = field(default="CreateNamespace")


@define(kw_only=True)
@router.delete(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/namespaces/{namespace}"
)
class DeleteNamespaceAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        namespace: str = field(metadata={"description": "The specified namespace."})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteNamespace")


@define(kw_only=True)
@router.get(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/namespaces/{namespace}"
)
class DescribeNamespaceAPI_1(BaseAPI[V1Namespace]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        namespace: str = field(metadata={"description": "The specified namespace."})

    path_params: PathParams
    response: Optional[V1Namespace] = field(default=V1Namespace)
    endpoint_id: Optional[str] = field(default="DescribeNamespace")


@define(kw_only=True)
@router.patch(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/namespaces/{namespace}"
)
class PatchNamespaceAPI(BaseAPI[V1Namespace]):
    """Patch the specified namespace in workspace."""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        namespace: str = field(metadata={"description": "The specified namespace."})

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
        metadata: Optional[V1ObjectMeta] = field(
            default=None,
            metadata={
                "description": "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
            },
        )
        spec: Optional[V1NamespaceSpec] = field(
            default=None,
            metadata={
                "description": "Spec defines the behavior of the Namespace. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
            },
        )
        status: Optional[V1NamespaceStatus] = field(
            default=None,
            metadata={
                "description": "Status describes the current status of a Namespace. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
            },
        )

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1Namespace] = field(default=V1Namespace)
    endpoint_id: Optional[str] = field(default="PatchNamespace")


@define(kw_only=True)
@router.put(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/namespaces/{namespace}"
)
class UpdateNamespaceAPI(BaseAPI[V1Namespace]):
    """Update namespace"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        namespace: str = field(metadata={"description": "The specified namespace."})

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
        metadata: Optional[V1ObjectMeta] = field(
            default=None,
            metadata={
                "description": "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
            },
        )
        spec: Optional[V1NamespaceSpec] = field(
            default=None,
            metadata={
                "description": "Spec defines the behavior of the Namespace. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
            },
        )
        status: Optional[V1NamespaceStatus] = field(
            default=None,
            metadata={
                "description": "Status describes the current status of a Namespace. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
            },
        )

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1Namespace] = field(default=V1Namespace)
    endpoint_id: Optional[str] = field(default="UpdateNamespace")


@define(kw_only=True)
@router.post(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/resourcequotas"
)
class CreateWorkspaceResourceQuotaAPI(BaseAPI[V1alpha2ResourceQuota]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    @define
    class RequestBodyModel:
        spec: V1alpha2ResourceQuotaSpec = field()
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
        status: Optional[V1alpha2ResourceQuotaStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1alpha2ResourceQuota] = field(default=V1alpha2ResourceQuota)
    endpoint_id: Optional[str] = field(default="CreateWorkspaceResourceQuota")


@define(kw_only=True)
@router.delete(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/resourcequotas/{resourcequota}"
)
class DeleteWorkspaceResourceQuotaAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        resourcequota: str = field(metadata={"description": "resource quota name"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteWorkspaceResourceQuota")


@define(kw_only=True)
@router.get(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/resourcequotas/{resourcequota}"
)
class DescribeWorkspaceResourceQuotaAPI(BaseAPI[V1alpha2ResourceQuota]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        resourcequota: str = field(metadata={"description": "Resource quota name"})

    path_params: PathParams
    response: Optional[V1alpha2ResourceQuota] = field(default=V1alpha2ResourceQuota)
    endpoint_id: Optional[str] = field(default="DescribeWorkspaceResourceQuota")


@define(kw_only=True)
@router.put(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/resourcequotas/{resourcequota}"
)
class UpdateWorkspaceResourceQuotaAPI(BaseAPI[V1alpha2ResourceQuota]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        resourcequota: str = field(metadata={"description": "Resource quota name"})

    @define
    class RequestBodyModel:
        spec: V1alpha2ResourceQuotaSpec = field()
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
        status: Optional[V1alpha2ResourceQuotaStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1alpha2ResourceQuota] = field(default=V1alpha2ResourceQuota)
    endpoint_id: Optional[str] = field(default="UpdateWorkspaceResourceQuota")


@define(kw_only=True)
@router.get(
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/workspacemembers/{workspacemember}/namespaces"
)
class ListNamespacesWorkspaceMemberAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        workspacemember: str = field(
            metadata={"description": "workspacemember username"}
        )

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="list-namespaces-workspace-member")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates")
class ListWorkspaceTemplatesAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used to do filtering"}
        )
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="list-workspace-templates")


@define(kw_only=True)
@router.post("/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates")
class CreateWorkspaceTemplateAPI(BaseAPI[V1beta1WorkspaceTemplate]):
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
        spec: Optional[V1beta1WorkspaceTemplateSpec] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="create-workspace-template")


@define(kw_only=True)
@router.delete("/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates/{workspace}")
class DeleteWorkspaceTemplateAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="delete-workspace-template")


@define(kw_only=True)
@router.get("/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates/{workspace}")
class GetWorkspaceTemplateAPI(BaseAPI[V1beta1WorkspaceTemplate]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    path_params: PathParams
    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="get-workspace-template")


@define(kw_only=True)
@router.patch("/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates/{workspace}")
class PatchWorkspaceTemplateAPI(BaseAPI[V1beta1WorkspaceTemplate]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

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
        spec: Optional[V1beta1WorkspaceTemplateSpec] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="patch-workspace-template")


@define(kw_only=True)
@router.put("/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates/{workspace}")
class UpdateWorkspaceTemplateAPI(BaseAPI[V1beta1WorkspaceTemplate]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

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
        spec: Optional[V1beta1WorkspaceTemplateSpec] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1beta1WorkspaceTemplate] = field(
        default=V1beta1WorkspaceTemplate
    )
    endpoint_id: Optional[str] = field(default="update-workspace-template")
