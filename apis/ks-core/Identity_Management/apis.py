from typing import Optional
from attrs import define, field
from .models import (
    ApiListResult,
    V1beta1UserStatus,
    V1beta1User,
    V1beta1UserSpec,
    V1ObjectMeta,
    ErrorsError,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "ListUsersAPI",
    "CreateUserAPI",
    "DeleteUserAPI",
    "DescribeUserAPI",
    "UpdateUserAPI",
    "ListUserLoginRecordsAPI",
    "ModifyPasswordAPI",
]


@define(kw_only=True)
@router.get("/kapis/iam.kubesphere.io/v1beta1/users")
class ListUsersAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        globalrole: Optional[str] = field(
            default=None, metadata={"description": "specific golalrole name"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListUsers")


@define(kw_only=True)
@router.post("/kapis/iam.kubesphere.io/v1beta1/users")
class CreateUserAPI(BaseAPI[V1beta1User]):
    """None"""

    @define
    class RequestBodyModel:
        spec: V1beta1UserSpec = field()
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
        status: Optional[V1beta1UserStatus] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V1beta1User] = field(default=V1beta1User)
    endpoint_id: Optional[str] = field(default="CreateUser")


@define(kw_only=True)
@router.delete("/kapis/iam.kubesphere.io/v1beta1/users/{user}")
class DeleteUserAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "username"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteUser")


@define(kw_only=True)
@router.get("/kapis/iam.kubesphere.io/v1beta1/users/{user}")
class DescribeUserAPI(BaseAPI[V1beta1User]):
    """Retrieve user details."""

    @define
    class PathParams:
        user: str = field(metadata={"description": "username"})

    path_params: PathParams
    response: Optional[V1beta1User] = field(default=V1beta1User)
    endpoint_id: Optional[str] = field(default="DescribeUser")


@define(kw_only=True)
@router.put("/kapis/iam.kubesphere.io/v1beta1/users/{user}")
class UpdateUserAPI(BaseAPI[V1beta1User]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "username"})

    @define
    class RequestBodyModel:
        spec: V1beta1UserSpec = field()
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
        status: Optional[V1beta1UserStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1beta1User] = field(default=V1beta1User)
    endpoint_id: Optional[str] = field(default="UpdateUser")


@define(kw_only=True)
@router.get("/kapis/iam.kubesphere.io/v1beta1/users/{user}/loginrecords")
class ListUserLoginRecordsAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "username of the user"})

    path_params: PathParams
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListUserLoginRecords")


@define(kw_only=True)
@router.put("/kapis/iam.kubesphere.io/v1beta1/users/{user}/password")
class ModifyPasswordAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "username"})

    @define
    class RequestBodyModel:
        currentPassword: str = field()
        password: str = field()

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="ModifyPassword")
