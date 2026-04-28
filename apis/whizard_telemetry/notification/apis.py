from typing import Optional
from attrs import define, field
from .models import ApiListResult, ErrorsError
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "ListResourceAPI",
    "CreateResourceAPI",
    "GetResourceAPI",
    "UpdateResourceAPI",
    "DeleteResourceAPI",
    "PatchResourceAPI",
    "ListResourceAPI_1",
    "CreateResourceAPI_1",
    "GetResourceAPI_1",
    "UpdateResourceAPI_1",
    "DeleteResourceAPI_1",
    "PatchResourceAPI_1",
]


@define(kw_only=True)
@router.get("/kapis/notification.kubesphere.io/v2beta2/users/{user}/{resources}")
class ListResourceAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "user name"})
        resources: str = field(
            metadata={
                "description": "known values include configs, receivers, secrets, silences, configmaps"
            }
        )

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used for filtering"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector used for filtering"}
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "description": "config or receiver type, known values include dingtalk, email, feishu, slack, webhook, wechat"
            },
        )
        page: Optional[str] = field(default="page=1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="ascending=false",
            metadata={"description": "sort parameters, e.g. ascending=false"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListResource")


@define(kw_only=True)
@router.post("/kapis/notification.kubesphere.io/v2beta2/users/{user}/{resources}")
class CreateResourceAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "user name"})
        resources: str = field(
            metadata={
                "description": "known values include configs, receivers, secrets, silences, configmaps"
            }
        )

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateResource")


@define(kw_only=True)
@router.get("/kapis/notification.kubesphere.io/v2beta2/users/{user}/{resources}/{name}")
class GetResourceAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "user name"})
        resources: str = field(
            metadata={
                "description": "known values include configs, receivers, secrets, silences, configmaps"
            }
        )
        name: str = field(metadata={"description": "the name of the resource"})

    @define
    class QueryParams:
        type: Optional[str] = field(
            default=None,
            metadata={
                "description": "config or receiver type, known values include dingtalk, email, feishu, slack, webhook, wechat"
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="GetResource")


@define(kw_only=True)
@router.put("/kapis/notification.kubesphere.io/v2beta2/users/{user}/{resources}/{name}")
class UpdateResourceAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "user name"})
        resources: str = field(
            metadata={
                "description": "known values include configs, receivers, secrets, silences, configmaps"
            }
        )
        name: str = field(metadata={"description": "the name of the resource"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="UpdateResource")


@define(kw_only=True)
@router.delete(
    "/kapis/notification.kubesphere.io/v2beta2/users/{user}/{resources}/{name}"
)
class DeleteResourceAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "user name"})
        resources: str = field(
            metadata={
                "description": "known values include configs, receivers, secrets, silences, configmaps"
            }
        )
        name: str = field(metadata={"description": "the name of the resource"})

    @define
    class QueryParams:
        type: Optional[str] = field(
            default=None,
            metadata={
                "description": "config or receiver type, known values include dingtalk, email, feishu, slack, webhook, wechat"
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteResource")


@define(kw_only=True)
@router.patch(
    "/kapis/notification.kubesphere.io/v2beta2/users/{user}/{resources}/{name}"
)
class PatchResourceAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "user name"})
        resources: str = field(
            metadata={
                "description": "known values include configs, receivers, secrets, silences, configmaps"
            }
        )
        name: str = field(metadata={"description": "the name of the resource"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="PatchResource")


@define(kw_only=True)
@router.get("/kapis/notification.kubesphere.io/v2beta2/{resources}")
class ListResourceAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        resources: str = field(
            metadata={
                "description": "known values include notificationmanagers, configs, receivers, secrets, routers, silences, configmaps"
            }
        )

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used for filtering"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector used for filtering"}
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "description": "config or receiver type, known values include dingtalk, email, feishu, slack, webhook, wechat"
            },
        )
        page: Optional[str] = field(default="page=1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="ascending=false",
            metadata={"description": "sort parameters, e.g. ascending=false"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListResource")


@define(kw_only=True)
@router.post("/kapis/notification.kubesphere.io/v2beta2/{resources}")
class CreateResourceAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        resources: str = field(
            metadata={
                "description": "known values include notificationmanagers, configs, receivers, secrets, routers, silences, configmaps"
            }
        )

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateResource")


@define(kw_only=True)
@router.get("/kapis/notification.kubesphere.io/v2beta2/{resources}/{name}")
class GetResourceAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        resources: str = field(
            metadata={
                "description": "known values include notificationmanagers, configs, receivers, secrets, routers, silences, configmaps"
            }
        )
        name: str = field(metadata={"description": "the name of the resource"})

    @define
    class QueryParams:
        type: Optional[str] = field(
            default=None,
            metadata={
                "description": "config or receiver type, known values include dingtalk, feishu, email, slack, webhook, wechat"
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="GetResource")


@define(kw_only=True)
@router.put("/kapis/notification.kubesphere.io/v2beta2/{resources}/{name}")
class UpdateResourceAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        resources: str = field(
            metadata={
                "description": "known values include notificationmanagers, configs, receivers, secrets, routers, silences, configmaps"
            }
        )
        name: str = field(metadata={"description": "the name of the resource"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="UpdateResource")


@define(kw_only=True)
@router.delete("/kapis/notification.kubesphere.io/v2beta2/{resources}/{name}")
class DeleteResourceAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        resources: str = field(
            metadata={
                "description": "known values include configs, receivers, secrets, routers, silences, configmaps"
            }
        )
        name: str = field(metadata={"description": "the name of the resource"})

    @define
    class QueryParams:
        type: Optional[str] = field(
            default=None,
            metadata={
                "description": "config or receiver type, known values include dingtalk, email, feishu, slack, webhook, wechat"
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteResource")


@define(kw_only=True)
@router.patch("/kapis/notification.kubesphere.io/v2beta2/{resources}/{name}")
class PatchResourceAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        resources: str = field(
            metadata={
                "description": "known values include notificationmanagers, configs, receivers, secrets, routers, silences, configmaps"
            }
        )
        name: str = field(metadata={"description": "the name of the resource"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="PatchResource")
