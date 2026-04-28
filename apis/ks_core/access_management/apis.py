from typing import Optional, List
from attrs import define, field
from .models import (
    ApiListResult,
    V1beta1Member,
    ErrorsError,
    V1beta1SubjectAccessReviewSpec,
    V1beta1SubjectAccessReview,
    V1beta1SubjectAccessReviewStatus,
    V1beta1User,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "ListClusterMembersAPI",
    "CreateClusterMembersAPI",
    "RemoveClusterMemberAPI",
    "UpdateClusterMemberAPI",
    "ListNamespaceMembersAPI",
    "CreateNamespaceMembersAPI",
    "RemoveNamespaceMemberAPI",
    "UpdateNamespaceMemberAPI",
    "CreateSelfSubjectAccessReviewAPI",
    "CreateSubjectAccessReviewAPI",
    "ListRoleTemplateOfUserAPI",
    "ListWorkspaceMembersAPI",
    "CreateWorkspaceMembersAPI",
    "RemoveWorkspaceMemberAPI",
    "DescribeWorkspaceMemberAPI",
    "UpdateWorkspaceMemberAPI",
]


@define(kw_only=True)
@router.get("/kapis/iam.kubesphere.io/v1beta1/clustermembers")
class ListClusterMembersAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        clusterrole: Optional[str] = field(
            default=None, metadata={"description": "specific the cluster role name"}
        )
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
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )
        fieldSelector: Optional[str] = field(
            default=None, metadata={"description": "field selector used for filtering"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListClusterMembers")


@define(kw_only=True)
@router.post("/kapis/iam.kubesphere.io/v1beta1/clustermembers")
class CreateClusterMembersAPI(BaseAPI[V1beta1Member]):
    """None"""

    request_body: List[V1beta1Member] = field()

    response: Optional[V1beta1Member] = field(default=V1beta1Member)
    endpoint_id: Optional[str] = field(default="CreateClusterMembers")


@define(kw_only=True)
@router.delete("/kapis/iam.kubesphere.io/v1beta1/clustermembers/{clustermember}")
class RemoveClusterMemberAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        clustermember: str = field(
            metadata={"description": "cluster member's username"}
        )

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="RemoveClusterMember")


@define(kw_only=True)
@router.put("/kapis/iam.kubesphere.io/v1beta1/clustermembers/{clustermember}")
class UpdateClusterMemberAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        clustermember: str = field(
            metadata={"description": "the member name from cluster"}
        )

    @define
    class RequestBodyModel:
        roleRef: str = field()
        username: str = field()

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="UpdateClusterMember")


@define(kw_only=True)
@router.get("/kapis/iam.kubesphere.io/v1beta1/namespaces/{namespace}/namespacemembers")
class ListNamespaceMembersAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    @define
    class QueryParams:
        role: Optional[str] = field(
            default=None, metadata={"description": "specific the role name"}
        )
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
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )
        fieldSelector: Optional[str] = field(
            default=None, metadata={"description": "field selector used for filtering"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListNamespaceMembers")


@define(kw_only=True)
@router.post("/kapis/iam.kubesphere.io/v1beta1/namespaces/{namespace}/namespacemembers")
class CreateNamespaceMembersAPI(BaseAPI[V1beta1Member]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    request_body: List[V1beta1Member] = field()

    path_params: PathParams
    response: Optional[V1beta1Member] = field(default=V1beta1Member)
    endpoint_id: Optional[str] = field(default="CreateNamespaceMembers")


@define(kw_only=True)
@router.delete(
    "/kapis/iam.kubesphere.io/v1beta1/namespaces/{namespace}/namespacemembers/{member}"
)
class RemoveNamespaceMemberAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})
        member: str = field(metadata={"description": "namespace member's username"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="RemoveNamespaceMember")


@define(kw_only=True)
@router.put(
    "/kapis/iam.kubesphere.io/v1beta1/namespaces/{namespace}/namespacemembers/{namespacemember}"
)
class UpdateNamespaceMemberAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})
        namespacemember: str = field(
            metadata={"description": "the member from namespace"}
        )

    @define
    class RequestBodyModel:
        roleRef: str = field()
        username: str = field()

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="UpdateNamespaceMember")


@define(kw_only=True)
@router.post("/kapis/iam.kubesphere.io/v1beta1/selfsubjectaccessreviews")
class CreateSelfSubjectAccessReviewAPI(BaseAPI[V1beta1SubjectAccessReview]):
    """Evaluates all current user's request attributes against all policies and allows or denies the request."""

    @define
    class RequestBodyModel:
        spec: V1beta1SubjectAccessReviewSpec = field()
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
        status: Optional[V1beta1SubjectAccessReviewStatus] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V1beta1SubjectAccessReview] = field(
        default=V1beta1SubjectAccessReview
    )
    endpoint_id: Optional[str] = field(default="CreateSelfSubjectAccessReview")


@define(kw_only=True)
@router.post("/kapis/iam.kubesphere.io/v1beta1/subjectaccessreviews")
class CreateSubjectAccessReviewAPI(BaseAPI[V1beta1SubjectAccessReview]):
    """Evaluates all of the request attributes against all policies and allows or denies the request."""

    @define
    class RequestBodyModel:
        spec: V1beta1SubjectAccessReviewSpec = field()
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
        status: Optional[V1beta1SubjectAccessReviewStatus] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V1beta1SubjectAccessReview] = field(
        default=V1beta1SubjectAccessReview
    )
    endpoint_id: Optional[str] = field(default="CreateSubjectAccessReview")


@define(kw_only=True)
@router.get("/kapis/iam.kubesphere.io/v1beta1/users/{username}/roletemplates")
class ListRoleTemplateOfUserAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        username: str = field(
            metadata={"description": "the name of the specified user"}
        )

    @define
    class QueryParams:
        scope: Optional[str] = field(
            default=None, metadata={"description": "the scope of role templates"}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "the namespace of role templates"}
        )
        workspace: Optional[str] = field(
            default=None, metadata={"description": "the workspace of role templates"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListRoleTemplateOfUser")


@define(kw_only=True)
@router.get("/kapis/iam.kubesphere.io/v1beta1/workspaces/{workspace}/workspacemembers")
class ListWorkspaceMembersAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    @define
    class QueryParams:
        workspacerole: Optional[str] = field(
            default=None, metadata={"description": "specific the workspace role name"}
        )
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
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )
        fieldSelector: Optional[str] = field(
            default=None, metadata={"description": "field selector used for filtering"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListWorkspaceMembers")


@define(kw_only=True)
@router.post("/kapis/iam.kubesphere.io/v1beta1/workspaces/{workspace}/workspacemembers")
class CreateWorkspaceMembersAPI(BaseAPI[V1beta1Member]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})

    request_body: List[V1beta1Member] = field()

    path_params: PathParams
    response: Optional[V1beta1Member] = field(default=V1beta1Member)
    endpoint_id: Optional[str] = field(default="CreateWorkspaceMembers")


@define(kw_only=True)
@router.delete(
    "/kapis/iam.kubesphere.io/v1beta1/workspaces/{workspace}/workspacemembers/{workspacemember}"
)
class RemoveWorkspaceMemberAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        workspacemember: str = field(
            metadata={"description": "Workspace member's name."}
        )

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="RemoveWorkspaceMember")


@define(kw_only=True)
@router.get(
    "/kapis/iam.kubesphere.io/v1beta1/workspaces/{workspace}/workspacemembers/{workspacemember}"
)
class DescribeWorkspaceMemberAPI(BaseAPI[V1beta1User]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        workspacemember: str = field(
            metadata={"description": "Workspace member's name."}
        )

    path_params: PathParams
    response: Optional[V1beta1User] = field(default=V1beta1User)
    endpoint_id: Optional[str] = field(default="DescribeWorkspaceMember")


@define(kw_only=True)
@router.put(
    "/kapis/iam.kubesphere.io/v1beta1/workspaces/{workspace}/workspacemembers/{workspacemember}"
)
class UpdateWorkspaceMemberAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "The specified workspace."})
        workspacemember: str = field(
            metadata={"description": "the member from workspace"}
        )

    @define
    class RequestBodyModel:
        roleRef: str = field()
        username: str = field()

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="UpdateWorkspaceMember")
