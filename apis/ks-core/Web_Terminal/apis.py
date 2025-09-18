from typing import Optional
from attrs import define, field
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "CreatePodExecAPI",
    "DownloadFileFromPodAPI",
    "UploadFileToPodAPI",
    "CreateNodeExecAPI",
    "CreateUserKubectlPodExecAPI",
]


@define(kw_only=True)
@router.get(
    "/kapis/terminal.kubesphere.io/v1alpha2/namespaces/{namespace}/pods/{pod}/exec"
)
class CreatePodExecAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})
        pod: str = field(metadata={"description": "pod name"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="create-pod-exec")


@define(kw_only=True)
@router.get(
    "/kapis/terminal.kubesphere.io/v1alpha2/namespaces/{namespace}/pods/{pod}/file"
)
class DownloadFileFromPodAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})
        pod: str = field(metadata={"description": "pod name"})

    @define
    class QueryParams:
        container: Optional[str] = field(
            default=None, metadata={"description": "container name"}
        )
        path: Optional[str] = field(default=None, metadata={"description": "file path"})

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="download-file-from-pod")


@define(kw_only=True)
@router.post(
    "/kapis/terminal.kubesphere.io/v1alpha2/namespaces/{namespace}/pods/{pod}/file"
)
class UploadFileToPodAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})
        pod: str = field(metadata={"description": "pod name"})

    @define
    class QueryParams:
        container: Optional[str] = field(
            default=None, metadata={"description": "container name"}
        )
        path: Optional[str] = field(
            default=None, metadata={"description": "dest dir path"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="upload-file-to-pod")


@define(kw_only=True)
@router.get("/kapis/terminal.kubesphere.io/v1alpha2/nodes/{nodename}/exec")
class CreateNodeExecAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        nodename: str = field(metadata={"description": "node name"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="create-node-exec")


@define(kw_only=True)
@router.get("/kapis/terminal.kubesphere.io/v1alpha2/users/{user}/kubectl")
class CreateUserKubectlPodExecAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "username"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="create-user-kubectl-pod-exec")
