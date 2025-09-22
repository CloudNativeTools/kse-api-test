from typing import Optional
from attrs import define, field
from .models import ErrorsError, V1SecretReference, RegistriesImageDetails
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "JobReRunAPI",
    "VerifyGitCredentialAPI",
    "GetRegistryEntryAPI",
    "VerifyRegistryCredentialAPI",
]


@define(kw_only=True)
@router.post(
    "/kapis/operations.kubesphere.io/v1alpha2/namespaces/{namespace}/jobs/{job}"
)
class JobReRunAPI(BaseAPI[ErrorsError]):
    """Rerun job whether the job is complete or not."""

    @define
    class PathParams:
        job: str = field(metadata={"description": "job name"})
        namespace: str = field(metadata={"description": "The specified namespace."})

    @define
    class QueryParams:
        resourceVersion: str = field(
            metadata={"description": "version of job, rerun when the version matches"}
        )
        action: Optional[str] = field(
            default=None, metadata={"description": 'action must be "rerun"'}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="JobReRun")


@define(kw_only=True)
@router.post("/kapis/resources.kubesphere.io/v1alpha2/git/verify")
class VerifyGitCredentialAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class RequestBodyModel:
        remoteUrl: str = field(metadata={"description": "git server url"})
        secretRef: Optional[V1SecretReference] = field(
            default=None, metadata={"description": "auth secret reference"}
        )

    request_body: RequestBodyModel

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="VerifyGitCredential")


@define(kw_only=True)
@router.get("/kapis/resources.kubesphere.io/v1alpha2/registry/blob")
class GetRegistryEntryAPI(BaseAPI[RegistriesImageDetails]):
    """None"""

    @define
    class QueryParams:
        image: str = field(
            metadata={"description": "query image, condition for filtering."}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "namespace which secret in."}
        )
        secret: Optional[str] = field(
            default=None, metadata={"description": "secret name"}
        )
        insecure: Optional[str] = field(
            default=None,
            metadata={"description": "whether verify cert if using https repo"},
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[RegistriesImageDetails] = field(default=RegistriesImageDetails)
    endpoint_id: Optional[str] = field(default="GetRegistryEntry")


@define(kw_only=True)
@router.post("/kapis/resources.kubesphere.io/v1alpha2/registry/verify")
class VerifyRegistryCredentialAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class RequestBodyModel:
        password: str = field(metadata={"description": "password"})
        serverhost: str = field(metadata={"description": "registry server host"})
        username: str = field(metadata={"description": "username"})

    request_body: RequestBodyModel

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="VerifyRegistryCredential")
