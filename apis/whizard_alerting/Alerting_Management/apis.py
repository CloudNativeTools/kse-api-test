from typing import Optional
from attrs import define, field
from .models import (
    ApiListResultV2beta1Alert,
    ApiListResultV2beta1ClusterRuleGroup,
    ApisV2beta1ClusterRuleGroupSpec,
    V2beta1RuleGroupStatus,
    V1ObjectMeta,
    V2beta1ClusterRuleGroup,
    ErrorsError,
    ApiListResultV2beta1RuleGroup,
    ApisV2beta1RuleGroupSpec,
    V2beta1RuleGroup,
    ApiListResultV2beta1GlobalRuleGroup,
    V2beta1GlobalRuleGroup,
    ApisV2beta1GlobalRuleGroupSpec,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "HandleListClusterAlertsAPI",
    "HandleListClusterRuleGroupsAPI",
    "HandleCreateClusterRuleGroupAPI",
    "HandleGetClusterRuleGroupAPI",
    "HandleUpdateClusterRuleGroupAPI",
    "HandleDeleteClusterRuleGroupAPI",
    "HandlePatchClusterRuleGroupAPI",
    "HandleListAlertsAPI",
    "HandleListRuleGroupsAPI",
    "HandleCreateRuleGroupAPI",
    "HandleGetRuleGroupAPI",
    "HandleUpdateRuleGroupAPI",
    "HandleDeleteRuleGroupAPI",
    "HandlePatchRuleGroupAPI",
    "HandleListGlobalAlertsAPI",
    "HandleListGlobalRuleGroupsAPI",
    "HandleCreateGlobalRuleGroupAPI",
    "HandleGetGlobalRuleGroupAPI",
    "HandleUpdateGlobalRuleGroupAPI",
    "HandleDeleteGlobalRuleGroupAPI",
    "HandlePatchGlobalRuleGroupAPI",
]


@define(kw_only=True)
@router.get("/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusteralerts")
class HandleListClusterAlertsAPI(BaseAPI[ApiListResultV2beta1Alert]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})

    @define
    class QueryParams:
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={
                "description": "sort parameters, one of `activeAt`. e.g. orderBy=activeAt"
            },
        )
        state: Optional[str] = field(
            default=None, metadata={"description": "state, one of `firing`, `pending`"}
        )
        label_filters: Optional[str] = field(
            default=None,
            metadata={
                "description": "label filters, concatenating multiple filters with commas, equal symbol for exact query, wave symbol for fuzzy query e.g. name~a"
            },
        )
        label_matcher: Optional[str] = field(
            default=None,
            metadata={
                "description": 'label matcher to match alert labels, follow prometheus matcher format. e.g. `{label_name1="valueA",label_name2=~"valueB|valueC"}`'
            },
        )
        builtin: Optional[str] = field(
            default=None,
            metadata={
                "description": "filter alerts, `true` for alerts from built-in rule groups and `false` for alerts from custom rule groups"
            },
        )
        keyword: Optional[str] = field(
            default=None, metadata={"description": "keyword to search alerts"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[type] = field(default=None)
    endpoint_id: Optional[str] = field(default="handleListClusterAlerts")


@define(kw_only=True)
@router.get("/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups")
class HandleListClusterRuleGroupsAPI(BaseAPI[ApiListResultV2beta1ClusterRuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})

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
        state: Optional[str] = field(
            default=None,
            metadata={
                "description": "filter rule groups which contain rules in specified state, one of `firing`, `pending`, `inactive`, `disabled`"
            },
        )
        builtin: Optional[str] = field(
            default=None,
            metadata={
                "description": "filter alerts, `true` for alerts from built-in rule groups and `false` for alerts from custom rule groups"
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[type] = field(default=None)
    endpoint_id: Optional[str] = field(default="handleListClusterRuleGroups")


@define(kw_only=True)
@router.post("/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups")
class HandleCreateClusterRuleGroupAPI(BaseAPI[V2beta1ClusterRuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})

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
        spec: Optional[ApisV2beta1ClusterRuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2beta1ClusterRuleGroup] = field(default=V2beta1ClusterRuleGroup)
    endpoint_id: Optional[str] = field(default="handleCreateClusterRuleGroup")


@define(kw_only=True)
@router.get(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups/{name}"
)
class HandleGetClusterRuleGroupAPI(BaseAPI[V2beta1ClusterRuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        name: str = field(
            metadata={"description": "The specified clusterrulegroup name."}
        )

    path_params: PathParams
    response: Optional[V2beta1ClusterRuleGroup] = field(default=V2beta1ClusterRuleGroup)
    endpoint_id: Optional[str] = field(default="handleGetClusterRuleGroup")


@define(kw_only=True)
@router.put(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups/{name}"
)
class HandleUpdateClusterRuleGroupAPI(BaseAPI[V2beta1ClusterRuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        name: str = field(
            metadata={"description": "The specified clusterrulegroup name."}
        )

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
        spec: Optional[ApisV2beta1ClusterRuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2beta1ClusterRuleGroup] = field(default=V2beta1ClusterRuleGroup)
    endpoint_id: Optional[str] = field(default="handleUpdateClusterRuleGroup")


@define(kw_only=True)
@router.delete(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups/{name}"
)
class HandleDeleteClusterRuleGroupAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        name: str = field(
            metadata={"description": "The specified clusterrulegroup name."}
        )

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="handleDeleteClusterRuleGroup")


@define(kw_only=True)
@router.patch(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusterrulegroups/{name}"
)
class HandlePatchClusterRuleGroupAPI(BaseAPI[V2beta1ClusterRuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        name: str = field(
            metadata={"description": "The specified clusterrulegroup name."}
        )

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
        spec: Optional[ApisV2beta1ClusterRuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2beta1ClusterRuleGroup] = field(default=V2beta1ClusterRuleGroup)
    endpoint_id: Optional[str] = field(default="handlePatchClusterRuleGroup")


@define(kw_only=True)
@router.get(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/alerts"
)
class HandleListAlertsAPI(BaseAPI[ApiListResultV2beta1Alert]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        namespace: str = field(metadata={"description": "The specified namespace."})

    @define
    class QueryParams:
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={
                "description": "sort parameters, one of `activeAt`. e.g. orderBy=activeAt"
            },
        )
        state: Optional[str] = field(
            default=None, metadata={"description": "state, one of `firing`, `pending`"}
        )
        label_filters: Optional[str] = field(
            default=None,
            metadata={
                "description": "label filters, concatenating multiple filters with commas, equal symbol for exact query, wave symbol for fuzzy query e.g. name~a"
            },
        )
        label_matcher: Optional[str] = field(
            default=None,
            metadata={
                "description": 'label matcher to match alert labels, follow prometheus matcher format. e.g. `{label_name1="valueA",label_name2=~"valueB|valueC"}`'
            },
        )
        keyword: Optional[str] = field(
            default=None, metadata={"description": "keyword to search alerts"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResultV2beta1Alert] = field(
        default=ApiListResultV2beta1Alert
    )
    endpoint_id: Optional[str] = field(default="handleListAlerts")


@define(kw_only=True)
@router.get(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups"
)
class HandleListRuleGroupsAPI(BaseAPI[ApiListResultV2beta1RuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        namespace: str = field(metadata={"description": "The specified namespace."})

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
        state: Optional[str] = field(
            default=None,
            metadata={
                "description": "filter rule groups which contain rules in specified state, one of `firing`, `pending`, `inactive`, `disabled`"
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResultV2beta1RuleGroup] = field(
        default=ApiListResultV2beta1RuleGroup
    )
    endpoint_id: Optional[str] = field(default="handleListRuleGroups")


@define(kw_only=True)
@router.post(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups"
)
class HandleCreateRuleGroupAPI(BaseAPI[V2beta1RuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
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
        metadata: Optional[V1ObjectMeta] = field(default=None)
        spec: Optional[ApisV2beta1RuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2beta1RuleGroup] = field(default=V2beta1RuleGroup)
    endpoint_id: Optional[str] = field(default="handleCreateRuleGroup")


@define(kw_only=True)
@router.get(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups/{name}"
)
class HandleGetRuleGroupAPI(BaseAPI[V2beta1RuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        namespace: str = field(metadata={"description": "The specified namespace."})
        name: str = field(metadata={"description": "The specified rulegroup name."})

    path_params: PathParams
    response: Optional[V2beta1RuleGroup] = field(default=V2beta1RuleGroup)
    endpoint_id: Optional[str] = field(default="handleGetRuleGroup")


@define(kw_only=True)
@router.put(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups/{name}"
)
class HandleUpdateRuleGroupAPI(BaseAPI[V2beta1RuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        namespace: str = field(metadata={"description": "The specified namespace."})
        name: str = field(metadata={"description": "The specified rulegroup name."})

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
        spec: Optional[ApisV2beta1RuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2beta1RuleGroup] = field(default=V2beta1RuleGroup)
    endpoint_id: Optional[str] = field(default="handleUpdateRuleGroup")


@define(kw_only=True)
@router.delete(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups/{name}"
)
class HandleDeleteRuleGroupAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        namespace: str = field(metadata={"description": "The specified namespace."})
        name: str = field(metadata={"description": "The specified rulegroup name."})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="handleDeleteRuleGroup")


@define(kw_only=True)
@router.patch(
    "/alerting.kubesphere.io/v2beta1/clusters/{cluster}/namespaces/{namespace}/rulegroups/{name}"
)
class HandlePatchRuleGroupAPI(BaseAPI[V2beta1RuleGroup]):
    """None"""

    @define
    class PathParams:
        cluster: str = field(metadata={"description": "The specified cluster."})
        namespace: str = field(metadata={"description": "The specified namespace."})
        name: str = field(metadata={"description": "The specified rulegroup name."})

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
        spec: Optional[ApisV2beta1RuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2beta1RuleGroup] = field(default=V2beta1RuleGroup)
    endpoint_id: Optional[str] = field(default="handlePatchRuleGroup")


@define(kw_only=True)
@router.get("/alerting.kubesphere.io/v2beta1/globalalerts")
class HandleListGlobalAlertsAPI(BaseAPI[ApiListResultV2beta1Alert]):
    """None"""

    @define
    class QueryParams:
        page: Optional[str] = field(default="1", metadata={"description": "page"})
        limit: Optional[str] = field(default=None, metadata={"description": "limit"})
        ascending: Optional[str] = field(
            default="false",
            metadata={"description": "sort parameters, e.g. reverse=true"},
        )
        sortBy: Optional[str] = field(
            default=None,
            metadata={
                "description": "sort parameters, one of `activeAt`. e.g. orderBy=activeAt"
            },
        )
        state: Optional[str] = field(
            default=None, metadata={"description": "state, one of `firing`, `pending`"}
        )
        label_filters: Optional[str] = field(
            default=None,
            metadata={
                "description": "label filters, concatenating multiple filters with commas, equal symbol for exact query, wave symbol for fuzzy query e.g. name~a"
            },
        )
        label_matcher: Optional[str] = field(
            default=None,
            metadata={
                "description": 'label matcher to match alert labels, follow prometheus matcher format. e.g. `{label_name1="valueA",label_name2=~"valueB|valueC"}`'
            },
        )
        builtin: Optional[str] = field(
            default=None,
            metadata={
                "description": "filter alerts, `true` for alerts from built-in rule groups and `false` for alerts from custom rule groups"
            },
        )
        keyword: Optional[str] = field(
            default=None, metadata={"description": "keyword to search alerts"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResultV2beta1Alert] = field(
        default=ApiListResultV2beta1Alert
    )
    endpoint_id: Optional[str] = field(default="handleListGlobalAlerts")


@define(kw_only=True)
@router.get("/alerting.kubesphere.io/v2beta1/globalrulegroups")
class HandleListGlobalRuleGroupsAPI(BaseAPI[ApiListResultV2beta1GlobalRuleGroup]):
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
        state: Optional[str] = field(
            default=None,
            metadata={
                "description": "filter rule groups which contain rules in specified state, one of `firing`, `pending`, `inactive`, `disabled`"
            },
        )
        builtin: Optional[str] = field(
            default=None,
            metadata={
                "description": "filter rule groups, `true` for built-in rule groups and `false` for custom rule groups"
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResultV2beta1GlobalRuleGroup] = field(
        default=ApiListResultV2beta1GlobalRuleGroup
    )
    endpoint_id: Optional[str] = field(default="handleListGlobalRuleGroups")


@define(kw_only=True)
@router.post("/alerting.kubesphere.io/v2beta1/globalrulegroups")
class HandleCreateGlobalRuleGroupAPI(BaseAPI[V2beta1GlobalRuleGroup]):
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
        spec: Optional[ApisV2beta1GlobalRuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V2beta1GlobalRuleGroup] = field(default=V2beta1GlobalRuleGroup)
    endpoint_id: Optional[str] = field(default="handleCreateGlobalRuleGroup")


@define(kw_only=True)
@router.get("/alerting.kubesphere.io/v2beta1/globalrulegroups/{name}")
class HandleGetGlobalRuleGroupAPI(BaseAPI[V2beta1GlobalRuleGroup]):
    """None"""

    @define
    class PathParams:
        name: str = field(
            metadata={"description": "The specified globalrulegroup name."}
        )

    path_params: PathParams
    response: Optional[V2beta1GlobalRuleGroup] = field(default=V2beta1GlobalRuleGroup)
    endpoint_id: Optional[str] = field(default="handleGetGlobalRuleGroup")


@define(kw_only=True)
@router.put("/alerting.kubesphere.io/v2beta1/globalrulegroups/{name}")
class HandleUpdateGlobalRuleGroupAPI(BaseAPI[V2beta1GlobalRuleGroup]):
    """None"""

    @define
    class PathParams:
        name: str = field(
            metadata={"description": "The specified globalrulegroup name."}
        )

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
        spec: Optional[ApisV2beta1GlobalRuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2beta1GlobalRuleGroup] = field(default=V2beta1GlobalRuleGroup)
    endpoint_id: Optional[str] = field(default="handleUpdateGlobalRuleGroup")


@define(kw_only=True)
@router.delete("/alerting.kubesphere.io/v2beta1/globalrulegroups/{name}")
class HandleDeleteGlobalRuleGroupAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        name: str = field(
            metadata={"description": "The specified globalrulegroup name."}
        )

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="handleDeleteGlobalRuleGroup")


@define(kw_only=True)
@router.patch("/alerting.kubesphere.io/v2beta1/globalrulegroups/{name}")
class HandlePatchGlobalRuleGroupAPI(BaseAPI[V2beta1GlobalRuleGroup]):
    """None"""

    @define
    class PathParams:
        name: str = field(
            metadata={"description": "The specified globalrulegroup name."}
        )

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
        spec: Optional[ApisV2beta1GlobalRuleGroupSpec] = field(default=None)
        status: Optional[V2beta1RuleGroupStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2beta1GlobalRuleGroup] = field(default=V2beta1GlobalRuleGroup)
    endpoint_id: Optional[str] = field(default="handlePatchGlobalRuleGroup")
