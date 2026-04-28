from typing import Optional
from attrs import define, field
from .models import ApiListResult
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "ResetClusterRuleGroupAPI",
    "ResetRuleGroupAPI",
    "ListClusterRuleGroupAPI",
    "CreateClusterRuleGroupAPI",
    "GetClusterRuleGroupAPI",
    "UpdateClusterRuleGroupAPI",
    "DeleteClusterRuleGroupAPI",
    "PatchClusterRuleGroupAPI",
    "ListRuleGroupAPI",
    "CreateRuleGroupAPI",
    "GetRuleGroupAPI",
    "UpdateRuleGroupAPI",
    "DeleteRuleGroupAPI",
    "PatchRuleGroupAPI",
]


@define(kw_only=True)
@router.post("/kapis/logging.whizard.io/v1alpha1/builtins/clusterrulegroups/reset")
class ResetClusterRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="resetClusterRuleGroup")


@define(kw_only=True)
@router.post("/kapis/logging.whizard.io/v1alpha1/builtins/rulegroups/reset")
class ResetRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="resetRuleGroup")


@define(kw_only=True)
@router.get("/kapis/logging.whizard.io/v1alpha1/clusterrulegroups")
class ListClusterRuleGroupAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used for filtering"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector used for filtering"}
        )
        status: Optional[str] = field(
            default=None,
            metadata={"description": "filter by enabled status, true or false"},
        )
        builtin: Optional[str] = field(
            default=None,
            metadata={"description": "filter by builtin status, true or false"},
        )
        type: Optional[str] = field(
            default=None,
            metadata={"description": "filter by type, e.g. logs, events, auditing"},
        )
        page: Optional[str] = field(default="page=1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        sortBy: Optional[str] = field(
            default="orderBy=createTime",
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        ascending: Optional[str] = field(
            default="ascending=false",
            metadata={"description": "sort parameters, e.g. ascending=false"},
        )
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="listClusterRuleGroup")


@define(kw_only=True)
@router.post("/kapis/logging.whizard.io/v1alpha1/clusterrulegroups")
class CreateClusterRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="createClusterRuleGroup")


@define(kw_only=True)
@router.get("/kapis/logging.whizard.io/v1alpha1/clusterrulegroups/{name}")
class GetClusterRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        name: str = field(metadata={"description": "ClusterRuleGroup name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="getClusterRuleGroup")


@define(kw_only=True)
@router.put("/kapis/logging.whizard.io/v1alpha1/clusterrulegroups/{name}")
class UpdateClusterRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        name: str = field(metadata={"description": "ClusterRuleGroup name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="updateClusterRuleGroup")


@define(kw_only=True)
@router.delete("/kapis/logging.whizard.io/v1alpha1/clusterrulegroups/{name}")
class DeleteClusterRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        name: str = field(metadata={"description": "ClusterRuleGroup name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="deleteClusterRuleGroup")


@define(kw_only=True)
@router.patch("/kapis/logging.whizard.io/v1alpha1/clusterrulegroups/{name}")
class PatchClusterRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        name: str = field(metadata={"description": "ClusterRuleGroup name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="patchClusterRuleGroup")


@define(kw_only=True)
@router.get("/kapis/logging.whizard.io/v1alpha1/namespaces/{namespace}/rulegroups")
class ListRuleGroupAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace name"})

    @define
    class QueryParams:
        name: Optional[str] = field(
            default=None, metadata={"description": "name used for filtering"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector used for filtering"}
        )
        status: Optional[str] = field(
            default=None,
            metadata={"description": "filter by enabled status, true or false"},
        )
        builtin: Optional[str] = field(
            default=None,
            metadata={"description": "filter by builtin status, true or false"},
        )
        type: Optional[str] = field(
            default=None,
            metadata={"description": "filter by type, e.g. logs, events, auditing"},
        )
        page: Optional[str] = field(default="page=1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        sortBy: Optional[str] = field(
            default="orderBy=createTime",
            metadata={"description": "sort parameters, e.g. orderBy=createTime"},
        )
        ascending: Optional[str] = field(
            default="ascending=false",
            metadata={"description": "sort parameters, e.g. ascending=false"},
        )
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="listRuleGroup")


@define(kw_only=True)
@router.post("/kapis/logging.whizard.io/v1alpha1/namespaces/{namespace}/rulegroups")
class CreateRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="createRuleGroup")


@define(kw_only=True)
@router.get(
    "/kapis/logging.whizard.io/v1alpha1/namespaces/{namespace}/rulegroups/{name}"
)
class GetRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace name"})
        name: str = field(metadata={"description": "RuleGroup name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="getRuleGroup")


@define(kw_only=True)
@router.put(
    "/kapis/logging.whizard.io/v1alpha1/namespaces/{namespace}/rulegroups/{name}"
)
class UpdateRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace name"})
        name: str = field(metadata={"description": "RuleGroup name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="updateRuleGroup")


@define(kw_only=True)
@router.delete(
    "/kapis/logging.whizard.io/v1alpha1/namespaces/{namespace}/rulegroups/{name}"
)
class DeleteRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace name"})
        name: str = field(metadata={"description": "RuleGroup name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="deleteRuleGroup")


@define(kw_only=True)
@router.patch(
    "/kapis/logging.whizard.io/v1alpha1/namespaces/{namespace}/rulegroups/{name}"
)
class PatchRuleGroupAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace name"})
        name: str = field(metadata={"description": "RuleGroup name"})

    @define
    class QueryParams:
        clusterName: Optional[str] = field(
            default=None,
            metadata={"description": "cluster name, empty means host cluster"},
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="patchRuleGroup")
