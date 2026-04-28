from typing import Optional, Dict
from attrs import define, field
from .models import (
    ApiWorkloads,
    V1DaemonSet,
    V1ReplicaSet,
    ApiResourceQuota,
    V1StatefulSet,
    ApiListResult,
    V2ImageConfig,
    ImagesearchResults,
    OverviewMetricResults,
    V1Secret,
    V1ObjectMeta,
    V2RepositoryTags,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "GetNamespacedAbnormalWorkloadsAPI",
    "GetDaemonSetRevisionAPI",
    "GetDeploymentRevisionAPI",
    "GetNamespaceQuotasAPI",
    "GetStatefulSetRevisionAPI",
    "ListNamespacedResourcesAPI",
    "GetNamespacedResourceAPI",
    "GetImageConfigAPI",
    "SearchImagesAPI",
    "GetNamespaceOverviewAPI",
    "VerifyImageRepositorySecretAPI",
    "GetRepositoryTagsAPI",
]


@define(kw_only=True)
@router.get(
    "/kapis/resources.kubesphere.io/v1alpha2/namespaces/{namespace}/abnormalworkloads"
)
class GetNamespacedAbnormalWorkloadsAPI(BaseAPI[ApiWorkloads]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    path_params: PathParams
    response: Optional[ApiWorkloads] = field(default=ApiWorkloads)
    endpoint_id: Optional[str] = field(default="get-namespaced-abnormal-workloads")


@define(kw_only=True)
@router.get(
    "/kapis/resources.kubesphere.io/v1alpha2/namespaces/{namespace}/daemonsets/{daemonset}/revisions/{revision}"
)
class GetDaemonSetRevisionAPI(BaseAPI[V1DaemonSet]):
    """None"""

    @define
    class PathParams:
        daemonset: str = field(metadata={"description": "the name of the daemonset"})
        namespace: str = field(metadata={"description": "The specified namespace."})
        revision: str = field(metadata={"description": "the revision of the daemonset"})

    path_params: PathParams
    response: Optional[V1DaemonSet] = field(default=V1DaemonSet)
    endpoint_id: Optional[str] = field(default="GetDaemonSetRevision")


@define(kw_only=True)
@router.get(
    "/kapis/resources.kubesphere.io/v1alpha2/namespaces/{namespace}/deployments/{deployment}/revisions/{revision}"
)
class GetDeploymentRevisionAPI(BaseAPI[V1ReplicaSet]):
    """None"""

    @define
    class PathParams:
        deployment: str = field(metadata={"description": "the name of deployment"})
        namespace: str = field(metadata={"description": "The specified namespace."})
        revision: str = field(
            metadata={"description": "the revision of the deployment"}
        )

    path_params: PathParams
    response: Optional[V1ReplicaSet] = field(default=V1ReplicaSet)
    endpoint_id: Optional[str] = field(default="GetDeploymentRevision")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha2/namespaces/{namespace}/quotas")
class GetNamespaceQuotasAPI(BaseAPI[ApiResourceQuota]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    path_params: PathParams
    response: Optional[ApiResourceQuota] = field(default=ApiResourceQuota)
    endpoint_id: Optional[str] = field(default="GetNamespaceQuotas")


@define(kw_only=True)
@router.get(
    "/kapis/resources.kubesphere.io/v1alpha2/namespaces/{namespace}/statefulsets/{statefulset}/revisions/{revision}"
)
class GetStatefulSetRevisionAPI(BaseAPI[V1StatefulSet]):
    """None"""

    @define
    class PathParams:
        statefulset: str = field(
            metadata={"description": "the name of the statefulset"}
        )
        namespace: str = field(metadata={"description": "The specified namespace."})
        revision: str = field(
            metadata={"description": "the revision of the statefulset"}
        )

    path_params: PathParams
    response: Optional[V1StatefulSet] = field(default=V1StatefulSet)
    endpoint_id: Optional[str] = field(default="GetStatefulSetRevision")


@define(kw_only=True)
@router.get(
    "/kapis/resources.kubesphere.io/v1alpha3/namespaces/{namespace}/{resources}"
)
class ListNamespacedResourcesAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})
        resources: str = field(
            metadata={
                "description": "namespace level resource type, e.g. pods,jobs,configmaps,services."
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
        fieldSelector: Optional[str] = field(
            default=None,
            metadata={
                "description": "field selector used for filtering, you can use the = , == and != operators with field selectors( = and == mean the same thing), e.g. fieldSelector=type=kubernetes.io/dockerconfigjson, multiple separated by comma"
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="list-namespaced-resources")


@define(kw_only=True)
@router.get(
    "/kapis/resources.kubesphere.io/v1alpha3/namespaces/{namespace}/{resources}/{name}"
)
class GetNamespacedResourceAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})
        resources: str = field(
            metadata={
                "description": "namespace level resource type, e.g. pods,jobs,configmaps,services."
            }
        )
        name: str = field(metadata={"description": "the name of resource"})

    path_params: PathParams
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="get-namespaced-resource")


@define(kw_only=True)
@router.get(
    "/kapis/resources.kubesphere.io/v1alpha3/namespaces/{namespace}/imageconfig"
)
class GetImageConfigAPI(BaseAPI[V2ImageConfig]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    @define
    class QueryParams:
        image: str = field(
            metadata={
                "description": "Image name to query, e.g. kubesphere/ks-apiserver:v3.1.1"
            }
        )
        secret: Optional[str] = field(
            default=None,
            metadata={
                "description": "Secret name of the image repository credential, left empty means anonymous fetch."
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[V2ImageConfig] = field(default=V2ImageConfig)
    endpoint_id: Optional[str] = field(default="GetImageConfig")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha3/namespaces/{namespace}/images")
class SearchImagesAPI(BaseAPI[ImagesearchResults]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    @define
    class QueryParams:
        q: str = field(
            metadata={
                "description": "Search parameter for project and repository name."
            }
        )
        secret: Optional[str] = field(
            default=None,
            metadata={
                "description": "Secret name of the image repository credential, left empty means anonymous fetch."
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ImagesearchResults] = field(default=ImagesearchResults)
    endpoint_id: Optional[str] = field(default="SearchImages")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha3/namespaces/{namespace}/metrics")
class GetNamespaceOverviewAPI(BaseAPI[OverviewMetricResults]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    path_params: PathParams
    response: Optional[OverviewMetricResults] = field(default=OverviewMetricResults)
    endpoint_id: Optional[str] = field(default="GetNamespaceOverview")


@define(kw_only=True)
@router.post(
    "/kapis/resources.kubesphere.io/v1alpha3/namespaces/{namespace}/registrysecrets/{secret}/verify"
)
class VerifyImageRepositorySecretAPI(BaseAPI[V1Secret]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})
        secret: str = field(metadata={"description": "Name of the secret."})

    @define
    class RequestBodyModel:
        apiVersion: Optional[str] = field(
            default=None,
            metadata={
                "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
            },
        )
        data: Optional[Dict] = field(
            default=None,
            metadata={
                "description": "Data contains the secret data. Each key must consist of alphanumeric characters, '-', '_' or '.'. The serialized form of the secret data is a base64 encoded string, representing the arbitrary (possibly non-string) data value here. Described in https://tools.ietf.org/html/rfc4648#section-4"
            },
        )
        immutable: Optional[bool] = field(
            default=None,
            metadata={
                "description": "Immutable, if set to true, ensures that data stored in the Secret cannot be updated (only object metadata can be modified). If not set to true, the field can be modified at any time. Defaulted to nil."
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
        stringData: Optional[Dict] = field(
            default=None,
            metadata={
                "description": "stringData allows specifying non-binary secret data in string form. It is provided as a write-only input field for convenience. All keys and values are merged into the data field on write, overwriting any existing values. The stringData field is never output when reading from the API."
            },
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "description": "Used to facilitate programmatic handling of secret data. More info: https://kubernetes.io/docs/concepts/configuration/secret/#secret-types"
            },
        )

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1Secret] = field(default=V1Secret)
    endpoint_id: Optional[str] = field(default="VerifyImageRepositorySecret")


@define(kw_only=True)
@router.get(
    "/kapis/resources.kubesphere.io/v1alpha3/namespaces/{namespace}/repositorytags"
)
class GetRepositoryTagsAPI(BaseAPI[V2RepositoryTags]):
    """List repository tags, this is an experimental API, use it by your own caution."""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    @define
    class QueryParams:
        repository: str = field(
            metadata={"description": "Repository to query, e.g. calico/cni."}
        )
        secret: Optional[str] = field(
            default=None,
            metadata={
                "description": "Secret name of the image repository credential, left empty means anonymous fetch."
            },
        )
        page: Optional[str] = field(default="page=1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="ascending=false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[V2RepositoryTags] = field(default=V2RepositoryTags)
    endpoint_id: Optional[str] = field(default="GetRepositoryTags")
