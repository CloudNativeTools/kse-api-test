from typing import Optional, List, Any
from attrs import define, field
from .models import (
    ApiListResult,
    V1ObjectMeta,
    V2ApplicationReleaseStatus,
    ErrorsError,
    V2ApplicationReleaseSpec,
    V2ApplicationRelease,
    UnstructuredUnstructured,
    V2Application,
    V2Maintainer,
    V2RepoCredential,
    V2GroupVersionResource,
    V1Time,
    V2ApplicationVersion,
    V2Attachment,
    V2CategoryStatus,
    V2Category,
    V2CategorySpec,
    V2RepoSpec,
    V2RepoStatus,
    V2Repo,
    V1alpha2ClusterConnectionConfiguration,
    V1alpha2GenericClusterConfiguration,
    V1alpha2OAuthConfiguration,
    V1alpha2GenericPlatformConfiguration,
    V1alpha2IngressClassScope,
    LoaderBufferedFile,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "ListAppRlsAPI",
    "CreateOrUpdateAppRlsAPI",
    "DeleteAppRlsAPI",
    "DescribeAppRlsAPI",
    "CreateOrUpdateAppRlsAPI_1",
    "AppCrListAPI",
    "CreateOrUpdateCRAPI",
    "DeleteAppCrAPI",
    "DescribeAppCrAPI",
    "GetInstallJobLogAPI",
    "ListAppsAPI",
    "CreateOrUpdateAppAPI",
    "DeleteAppAPI",
    "DescribeAppAPI",
    "PatchAppAPI",
    "CreateOrUpdateAppAPI_1",
    "DoAppActionAPI",
    "ExampleCrAPI",
    "ListAppVersionsAPI",
    "CreateOrUpdateAppVersionAPI",
    "DeleteAppVersionAPI",
    "DescribeAppVersionAPI",
    "CreateOrUpdateAppVersionAPI_1",
    "AppVersionActionAPI",
    "GetAppVersionFilesAPI",
    "GetAppVersionPackageAPI",
    "CreateAttachmentAPI",
    "DeleteAttachmentsAPI",
    "DescribeAttachmentAPI",
    "ListCategoriesAPI",
    "CreateOrUpdateCategoryAPI",
    "DeleteCategoryAPI",
    "DescribeCategoryAPI",
    "CreateOrUpdateCategoryAPI_1",
    "ListAppRlsAPI_1",
    "CreateOrUpdateAppRlsAPI_2",
    "DeleteAppRlsAPI_1",
    "DescribeAppRlsAPI_1",
    "CreateOrUpdateAppRlsAPI_3",
    "AppCrListAPI_1",
    "CreateOrUpdateCRAPI_1",
    "DeleteAppCrAPI_1",
    "DescribeAppCrAPI_1",
    "GetInstallJobLogAPI_1",
    "ListReposAPI",
    "CreateOrUpdateRepoAPI",
    "DeleteRepoAPI",
    "DescribeRepoAPI",
    "CreateOrUpdateRepoAPI_1",
    "ManualSyncAPI",
    "ListRepoEventsAPI",
    "ListReviewsAPI",
    "ListAppRlsAPI_2",
    "CreateOrUpdateAppRlsAPI_4",
    "AppCrListAPI_2",
    "CreateOrUpdateCRAPI_2",
    "DeleteAppCrAPI_2",
    "DescribeAppCrAPI_2",
    "ListAppsAPI_1",
    "CreateOrUpdateAppAPI_2",
    "DeleteAppAPI_1",
    "DescribeAppAPI_1",
    "PatchAppAPI_1",
    "CreateOrUpdateAppAPI_3",
    "ExampleCrAPI_1",
    "ListAppVersionsAPI_1",
    "CreateOrUpdateAppVersionAPI_2",
    "DeleteAppVersionAPI_1",
    "DescribeAppVersionAPI_1",
    "CreateOrUpdateAppVersionAPI_3",
    "AppVersionActionAPI_1",
    "GetAppVersionFilesAPI_1",
    "GetAppVersionPackageAPI_1",
    "CreateAttachmentAPI_1",
    "DeleteAttachmentsAPI_1",
    "DescribeAttachmentAPI_1",
    "ListReposAPI_1",
    "CreateOrUpdateRepoAPI_2",
    "DeleteRepoAPI_1",
    "DescribeRepoAPI_1",
    "CreateOrUpdateRepoAPI_3",
    "ManualSyncAPI_1",
    "ListRepoEventsAPI_1",
    "ListClusterConnectionConfigurationAPI",
    "GetClusterConnectionConfigurationAPI",
    "GetGenericClusterConfigurationAPI",
    "GetMulticlusterConfigurationAPI",
    "GetMarketplaceConfigurationAPI",
    "GetOAuthConfigurationAPI",
    "GetThemeConfigurationAPI",
    "UpdateThemeConfigurationAPI",
    "CreatePlatformConfigurationAPI",
    "DeletePlatformConfigurationAPI",
    "GetPlatformConfigurationAPI",
    "PatchPlatformConfigurationAPI",
    "UpdatePlatformConfigurationAPI",
    "ListIngressClassScopesAPI",
    "ListExtensionVersionFilesAPI",
    "UploadImageAPI",
    "GetImageAPI",
]


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/applications")
class ListAppRlsAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        appID: Optional[str] = field(
            default=None, metadata={"description": "app ID for filtering"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
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

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListAppRls")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/applications")
class CreateOrUpdateAppRlsAPI(BaseAPI[ErrorsError]):
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
        spec: Optional[V2ApplicationReleaseSpec] = field(default=None)
        status: Optional[V2ApplicationReleaseStatus] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/applications/{application}")
class DeleteAppRlsAPI(BaseAPI[ErrorsError]):
    """None"""

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAppRls")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/applications/{application}")
class DescribeAppRlsAPI(BaseAPI[V2ApplicationRelease]):
    """None"""

    response: Optional[V2ApplicationRelease] = field(default=V2ApplicationRelease)
    endpoint_id: Optional[str] = field(default="DescribeAppRls")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/applications/{application}")
class CreateOrUpdateAppRlsAPI_1(BaseAPI[ErrorsError]):
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
        spec: Optional[V2ApplicationReleaseSpec] = field(default=None)
        status: Optional[V2ApplicationReleaseStatus] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/applications/{application}/cr")
class AppCrListAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
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

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="AppCrList")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/applications/{application}/cr")
class CreateOrUpdateCRAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateCR")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/applications/{application}/cr/{crname}"
)
class DeleteAppCrAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "resource namespace"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAppCr")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/applications/{application}/cr/{crname}"
)
class DescribeAppCrAPI(BaseAPI[UnstructuredUnstructured]):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "resource namespace"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[UnstructuredUnstructured] = field(
        default=UnstructuredUnstructured
    )
    endpoint_id: Optional[str] = field(default="DescribeAppCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/applications/{application}/log")
class GetInstallJobLogAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        type: str = field(
            metadata={"description": "log type, installation or uninstallation"}
        )
        follow: Optional[str] = field(
            default=None, metadata={"description": "follow log stream"}
        )
        container: Optional[str] = field(
            default=None, metadata={"description": "container name"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="GetInstallJobLog")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps")
class ListAppsAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
        )
        name: Optional[str] = field(
            default=None, metadata={"description": "name for filtering"}
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

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListApps")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps")
class CreateOrUpdateAppAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateApp")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/apps/{app}")
class DeleteAppAPI(BaseAPI[ErrorsError]):
    """None"""

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteApp")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}")
class DescribeAppAPI(BaseAPI[V2Application]):
    """None"""

    response: Optional[V2Application] = field(default=V2Application)
    endpoint_id: Optional[str] = field(default="DescribeApp")


@define(kw_only=True)
@router.patch("/kapis/application.kubesphere.io/v2/apps/{app}")
class PatchAppAPI(BaseAPI[V2Application]):
    """None"""

    @define
    class RequestBodyModel:
        abstraction: Optional[str] = field(default=None)
        aliasName: Optional[str] = field(default=None)
        appHome: Optional[str] = field(default=None)
        appName: Optional[str] = field(default=None)
        appStore: Optional[bool] = field(default=None)
        appType: Optional[str] = field(default=None)
        attachments: Optional[List[str]] = field(default=None)
        categoryName: Optional[str] = field(default=None)
        credential: Optional[V2RepoCredential] = field(default=None)
        description: Optional[str] = field(default=None)
        digest: Optional[str] = field(default=None)
        fromRepo: Optional[bool] = field(default=None)
        hasCrd: Optional[str] = field(default=None)
        icon: Optional[str] = field(default=None)
        maintainers: Optional[List[V2Maintainer]] = field(default=None)
        originalName: Optional[str] = field(default=None)
        package: Optional[str] = field(default=None)
        pullUrl: Optional[str] = field(default=None)
        repoName: Optional[str] = field(default=None)
        resources: Optional[List[V2GroupVersionResource]] = field(default=None)
        url: Optional[str] = field(default=None)
        versionName: Optional[str] = field(default=None)
        workspace: Optional[str] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V2Application] = field(default=V2Application)
    endpoint_id: Optional[str] = field(default="PatchApp")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}")
class CreateOrUpdateAppAPI_1(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateApp")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}/action")
class DoAppActionAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class RequestBodyModel:
        message: Optional[str] = field(default=None)
        state: Optional[str] = field(default=None)
        updated: Optional[V1Time] = field(default=None)
        userName: Optional[str] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DoAppAction")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/examplecr/{name}")
class ExampleCrAPI(BaseAPI[UnstructuredUnstructured]):
    """None"""

    response: Optional[UnstructuredUnstructured] = field(
        default=UnstructuredUnstructured
    )
    endpoint_id: Optional[str] = field(default="exampleCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/versions")
class ListAppVersionsAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
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

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListAppVersions")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}/versions")
class CreateOrUpdateAppVersionAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppVersion")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}")
class DeleteAppVersionAPI(BaseAPI[ErrorsError]):
    """None"""

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAppVersion")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}")
class DescribeAppVersionAPI(BaseAPI[V2ApplicationVersion]):
    """None"""

    response: Optional[V2ApplicationVersion] = field(default=V2ApplicationVersion)
    endpoint_id: Optional[str] = field(default="DescribeAppVersion")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}")
class CreateOrUpdateAppVersionAPI_1(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppVersion")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}/action")
class AppVersionActionAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class RequestBodyModel:
        message: Optional[str] = field(default=None)
        state: Optional[str] = field(default=None)
        updated: Optional[V1Time] = field(default=None)
        userName: Optional[str] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="AppVersionAction")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}/files")
class GetAppVersionFilesAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="GetAppVersionFiles")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}/package")
class GetAppVersionPackageAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="GetAppVersionPackage")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/attachments")
class CreateAttachmentAPI(BaseAPI[V2Attachment]):
    """None"""

    response: Optional[V2Attachment] = field(default=V2Attachment)
    endpoint_id: Optional[str] = field(default="CreateAttachment")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/attachments/{attachment}")
class DeleteAttachmentsAPI(BaseAPI[ErrorsError]):
    """None"""

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAttachments")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/attachments/{attachment}")
class DescribeAttachmentAPI(BaseAPI[V2Attachment]):
    """None"""

    response: Optional[V2Attachment] = field(default=V2Attachment)
    endpoint_id: Optional[str] = field(default="DescribeAttachment")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/categories")
class ListCategoriesAPI(BaseAPI[ApiListResult]):
    """None"""

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
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListCategories")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/categories")
class CreateOrUpdateCategoryAPI(BaseAPI[V2Category]):
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
        spec: Optional[V2CategorySpec] = field(default=None)
        status: Optional[V2CategoryStatus] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V2Category] = field(default=V2Category)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateCategory")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/categories/{category}")
class DeleteCategoryAPI(BaseAPI[ErrorsError]):
    """None"""

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteCategory")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/categories/{category}")
class DescribeCategoryAPI(BaseAPI[V2Category]):
    """None"""

    response: Optional[V2Category] = field(default=V2Category)
    endpoint_id: Optional[str] = field(default="DescribeCategory")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/categories/{category}")
class CreateOrUpdateCategoryAPI_1(BaseAPI[V2Category]):
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
        spec: Optional[V2CategorySpec] = field(default=None)
        status: Optional[V2CategoryStatus] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V2Category] = field(default=V2Category)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateCategory")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications")
class ListAppRlsAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    @define
    class QueryParams:
        appID: Optional[str] = field(
            default=None, metadata={"description": "app ID for filtering"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
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

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListAppRls")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications")
class CreateOrUpdateAppRlsAPI_2(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

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
        spec: Optional[V2ApplicationReleaseSpec] = field(default=None)
        status: Optional[V2ApplicationReleaseStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}"
)
class DeleteAppRlsAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAppRls")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}"
)
class DescribeAppRlsAPI_1(BaseAPI[V2ApplicationRelease]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    response: Optional[V2ApplicationRelease] = field(default=V2ApplicationRelease)
    endpoint_id: Optional[str] = field(default="DescribeAppRls")


@define(kw_only=True)
@router.post(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}"
)
class CreateOrUpdateAppRlsAPI_3(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

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
        spec: Optional[V2ApplicationReleaseSpec] = field(default=None)
        status: Optional[V2ApplicationReleaseStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}/cr"
)
class AppCrListAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
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

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="AppCrList")


@define(kw_only=True)
@router.post(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}/cr"
)
class CreateOrUpdateCRAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateCR")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}/cr/{crname}"
)
class DeleteAppCrAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "resource namespace"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAppCr")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}/cr/{crname}"
)
class DescribeAppCrAPI_1(BaseAPI[UnstructuredUnstructured]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "resource namespace"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[UnstructuredUnstructured] = field(
        default=UnstructuredUnstructured
    )
    endpoint_id: Optional[str] = field(default="DescribeAppCr")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}/log"
)
class GetInstallJobLogAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    @define
    class QueryParams:
        type: str = field(
            metadata={"description": "log type, installation or uninstallation"}
        )
        follow: Optional[str] = field(
            default=None, metadata={"description": "follow log stream"}
        )
        container: Optional[str] = field(
            default=None, metadata={"description": "container name"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="GetInstallJobLog")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/repos")
class ListReposAPI(BaseAPI[ApiListResult]):
    """None"""

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
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListRepos")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/repos")
class CreateOrUpdateRepoAPI(BaseAPI):
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
        spec: Optional[V2RepoSpec] = field(default=None)
        status: Optional[V2RepoStatus] = field(default=None)

    request_body: RequestBodyModel

    endpoint_id: Optional[str] = field(default="CreateOrUpdateRepo")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/repos/{repo}")
class DeleteRepoAPI(BaseAPI[ErrorsError]):
    """None"""

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteRepo")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/repos/{repo}")
class DescribeRepoAPI(BaseAPI[V2Repo]):
    """None"""

    response: Optional[V2Repo] = field(default=V2Repo)
    endpoint_id: Optional[str] = field(default="DescribeRepo")


@define(kw_only=True)
@router.patch("/kapis/application.kubesphere.io/v2/repos/{repo}")
class CreateOrUpdateRepoAPI_1(BaseAPI):
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
        spec: Optional[V2RepoSpec] = field(default=None)
        status: Optional[V2RepoStatus] = field(default=None)

    request_body: RequestBodyModel

    endpoint_id: Optional[str] = field(default="CreateOrUpdateRepo")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/repos/{repo}/action")
class ManualSyncAPI(BaseAPI[ErrorsError]):
    """None"""

    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="ManualSync")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/repos/{repo}/events")
class ListRepoEventsAPI(BaseAPI[ApiListResult]):
    """None"""

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
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListRepoEvents")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/reviews")
class ListReviewsAPI(BaseAPI[ApiListResult]):
    """None"""

    @define
    class QueryParams:
        status: Optional[str] = field(
            default=None,
            metadata={"description": "status for filtering, multiple separated by |"},
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

    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListReviews")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/applications")
class ListAppRlsAPI_2(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class QueryParams:
        appID: Optional[str] = field(
            default=None, metadata={"description": "app ID for filtering"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
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

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListAppRls")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/applications")
class CreateOrUpdateAppRlsAPI_4(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

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
        spec: Optional[V2ApplicationReleaseSpec] = field(default=None)
        status: Optional[V2ApplicationReleaseStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/applications/{application}/cr"
)
class AppCrListAPI_2(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
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

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="AppCrList")


@define(kw_only=True)
@router.post(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/applications/{application}/cr"
)
class CreateOrUpdateCRAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="CreateOrUpdateCR")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/applications/{application}/cr/{crname}"
)
class DeleteAppCrAPI_2(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "resource namespace"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAppCr")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/applications/{application}/cr/{crname}"
)
class DescribeAppCrAPI_2(BaseAPI[UnstructuredUnstructured]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class QueryParams:
        cluster: Optional[str] = field(
            default=None, metadata={"description": "cluster name"}
        )
        namespace: Optional[str] = field(
            default=None, metadata={"description": "resource namespace"}
        )
        group: Optional[str] = field(
            default=None, metadata={"description": "resource group"}
        )
        version: Optional[str] = field(
            default=None, metadata={"description": "resource version"}
        )
        resource: Optional[str] = field(
            default=None, metadata={"description": "resource name"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[UnstructuredUnstructured] = field(
        default=UnstructuredUnstructured
    )
    endpoint_id: Optional[str] = field(default="DescribeAppCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps")
class ListAppsAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class QueryParams:
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
        )
        name: Optional[str] = field(
            default=None, metadata={"description": "name for filtering"}
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

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListApps")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps")
class CreateOrUpdateAppAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateApp")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}")
class DeleteAppAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteApp")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}")
class DescribeAppAPI_1(BaseAPI[V2Application]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[V2Application] = field(default=V2Application)
    endpoint_id: Optional[str] = field(default="DescribeApp")


@define(kw_only=True)
@router.patch("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}")
class PatchAppAPI_1(BaseAPI[V2Application]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class RequestBodyModel:
        abstraction: Optional[str] = field(default=None)
        aliasName: Optional[str] = field(default=None)
        appHome: Optional[str] = field(default=None)
        appName: Optional[str] = field(default=None)
        appStore: Optional[bool] = field(default=None)
        appType: Optional[str] = field(default=None)
        attachments: Optional[List[str]] = field(default=None)
        categoryName: Optional[str] = field(default=None)
        credential: Optional[V2RepoCredential] = field(default=None)
        description: Optional[str] = field(default=None)
        digest: Optional[str] = field(default=None)
        fromRepo: Optional[bool] = field(default=None)
        hasCrd: Optional[str] = field(default=None)
        icon: Optional[str] = field(default=None)
        maintainers: Optional[List[V2Maintainer]] = field(default=None)
        originalName: Optional[str] = field(default=None)
        package: Optional[str] = field(default=None)
        pullUrl: Optional[str] = field(default=None)
        repoName: Optional[str] = field(default=None)
        resources: Optional[List[V2GroupVersionResource]] = field(default=None)
        url: Optional[str] = field(default=None)
        versionName: Optional[str] = field(default=None)
        workspace: Optional[str] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V2Application] = field(default=V2Application)
    endpoint_id: Optional[str] = field(default="PatchApp")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}")
class CreateOrUpdateAppAPI_3(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateApp")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/examplecr/{name}"
)
class ExampleCrAPI_1(BaseAPI[UnstructuredUnstructured]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[UnstructuredUnstructured] = field(
        default=UnstructuredUnstructured
    )
    endpoint_id: Optional[str] = field(default="exampleCr")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions"
)
class ListAppVersionsAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class QueryParams:
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector for filtering"}
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

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListAppVersions")


@define(kw_only=True)
@router.post(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions"
)
class CreateOrUpdateAppVersionAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppVersion")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions/{version}"
)
class DeleteAppVersionAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAppVersion")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions/{version}"
)
class DescribeAppVersionAPI_1(BaseAPI[V2ApplicationVersion]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[V2ApplicationVersion] = field(default=V2ApplicationVersion)
    endpoint_id: Optional[str] = field(default="DescribeAppVersion")


@define(kw_only=True)
@router.post(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions/{version}"
)
class CreateOrUpdateAppVersionAPI_3(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppVersion")


@define(kw_only=True)
@router.post(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions/{version}/action"
)
class AppVersionActionAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    @define
    class RequestBodyModel:
        message: Optional[str] = field(default=None)
        state: Optional[str] = field(default=None)
        updated: Optional[V1Time] = field(default=None)
        userName: Optional[str] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="AppVersionAction")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions/{version}/files"
)
class GetAppVersionFilesAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="GetAppVersionFiles")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions/{version}/package"
)
class GetAppVersionPackageAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="GetAppVersionPackage")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/attachments")
class CreateAttachmentAPI_1(BaseAPI[V2Attachment]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[V2Attachment] = field(default=V2Attachment)
    endpoint_id: Optional[str] = field(default="CreateAttachment")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/attachments/{attachment}"
)
class DeleteAttachmentsAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteAttachments")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/attachments/{attachment}"
)
class DescribeAttachmentAPI_1(BaseAPI[V2Attachment]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[V2Attachment] = field(default=V2Attachment)
    endpoint_id: Optional[str] = field(default="DescribeAttachment")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos")
class ListReposAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

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
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListRepos")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos")
class CreateOrUpdateRepoAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

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
        spec: Optional[V2RepoSpec] = field(default=None)
        status: Optional[V2RepoStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateRepo")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}"
)
class DeleteRepoAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="DeleteRepo")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}")
class DescribeRepoAPI_1(BaseAPI[V2Repo]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[V2Repo] = field(default=V2Repo)
    endpoint_id: Optional[str] = field(default="DescribeRepo")


@define(kw_only=True)
@router.patch("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}")
class CreateOrUpdateRepoAPI_3(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

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
        spec: Optional[V2RepoSpec] = field(default=None)
        status: Optional[V2RepoStatus] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateRepo")


@define(kw_only=True)
@router.post(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}/action"
)
class ManualSyncAPI_1(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="ManualSync")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}/events"
)
class ListRepoEventsAPI_1(BaseAPI[ApiListResult]):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

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
        labelSelector: Optional[str] = field(
            default=None, metadata={"description": "label selector"}
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[ApiListResult] = field(default=ApiListResult)
    endpoint_id: Optional[str] = field(default="ListRepoEvents")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/clusterconnectionconfigurations")
class ListClusterConnectionConfigurationAPI(
    BaseAPI[V1alpha2ClusterConnectionConfiguration]
):
    """Provides information about all cluster connection plugins"""

    response: Optional[V1alpha2ClusterConnectionConfiguration] = field(
        default=V1alpha2ClusterConnectionConfiguration
    )
    endpoint_id: Optional[str] = field(default="listClusterConnectionConfiguration")


@define(kw_only=True)
@router.get(
    "/kapis/config.kubesphere.io/v1alpha2/clusterconnectionconfigurations/{config}"
)
class GetClusterConnectionConfigurationAPI(
    BaseAPI[V1alpha2ClusterConnectionConfiguration]
):
    """Provides information about the cluster connection plugin"""

    @define
    class PathParams:
        config: str = field(metadata={"description": "config name"})

    path_params: PathParams
    response: Optional[V1alpha2ClusterConnectionConfiguration] = field(
        default=V1alpha2ClusterConnectionConfiguration
    )
    endpoint_id: Optional[str] = field(default="getClusterConnectionConfiguration")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/{config}")
class GetGenericClusterConfigurationAPI(BaseAPI[V1alpha2GenericClusterConfiguration]):
    """Provides the configuration details."""

    @define
    class PathParams:
        config: str = field(metadata={"description": "config name"})

    path_params: PathParams
    response: Optional[V1alpha2GenericClusterConfiguration] = field(
        default=V1alpha2GenericClusterConfiguration
    )
    endpoint_id: Optional[str] = field(default="getGenericClusterConfiguration")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/configz")
class GetMulticlusterConfigurationAPI(BaseAPI):
    """Provides information about the multicluster configuration."""

    endpoint_id: Optional[str] = field(default="getMulticlusterConfiguration")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/marketplace")
class GetMarketplaceConfigurationAPI(BaseAPI):
    """Provides the configuration details for the marketplace."""

    endpoint_id: Optional[str] = field(default="getMarketplaceConfiguration")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/oauth")
class GetOAuthConfigurationAPI(BaseAPI[V1alpha2OAuthConfiguration]):
    """Provides information about the authorization server."""

    response: Optional[V1alpha2OAuthConfiguration] = field(
        default=V1alpha2OAuthConfiguration
    )
    endpoint_id: Optional[str] = field(default="getOAuthConfiguration")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/configs/theme")
class GetThemeConfigurationAPI(BaseAPI):
    """Provides the current theme configuration details."""

    endpoint_id: Optional[str] = field(default="getThemeConfiguration")


@define(kw_only=True)
@router.put("/kapis/config.kubesphere.io/v1alpha2/configs/theme")
class UpdateThemeConfigurationAPI(BaseAPI):
    """Allows the user to update the theme configuration settings."""

    endpoint_id: Optional[str] = field(default="updateThemeConfiguration")


@define(kw_only=True)
@router.post("/kapis/config.kubesphere.io/v1alpha2/platformconfigs")
class CreatePlatformConfigurationAPI(BaseAPI[V1alpha2GenericPlatformConfiguration]):
    """Allows the user to create a new configuration for the specified platform."""

    @define
    class RequestBodyModel:
        apiVersion: Optional[str] = field(
            default=None,
            metadata={
                "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
            },
        )
        data: Optional[Any] = field(default=None)
        kind: Optional[str] = field(
            default=None,
            metadata={
                "description": "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
            },
        )
        metadata: Optional[V1ObjectMeta] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[V1alpha2GenericPlatformConfiguration] = field(
        default=V1alpha2GenericPlatformConfiguration
    )
    endpoint_id: Optional[str] = field(default="createPlatformConfiguration")


@define(kw_only=True)
@router.delete("/kapis/config.kubesphere.io/v1alpha2/platformconfigs/{config}")
class DeletePlatformConfigurationAPI(BaseAPI):
    """Allows the user to delete the configuration settings of the specified platform."""

    @define
    class PathParams:
        config: str = field(metadata={"description": "config name"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="deletePlatformConfiguration")


@define(kw_only=True)
@router.get("/kapis/config.kubesphere.io/v1alpha2/platformconfigs/{config}")
class GetPlatformConfigurationAPI(BaseAPI[V1alpha2GenericPlatformConfiguration]):
    """Provides details of the specified platform configuration."""

    @define
    class PathParams:
        config: str = field(metadata={"description": "config name"})

    path_params: PathParams
    response: Optional[V1alpha2GenericPlatformConfiguration] = field(
        default=V1alpha2GenericPlatformConfiguration
    )
    endpoint_id: Optional[str] = field(default="getPlatformConfiguration")


@define(kw_only=True)
@router.patch("/kapis/config.kubesphere.io/v1alpha2/platformconfigs/{config}")
class PatchPlatformConfigurationAPI(BaseAPI[V1alpha2GenericPlatformConfiguration]):
    """Allows the user to apply partial modifications to the configuration settings of the specified platform"""

    @define
    class PathParams:
        config: str = field(metadata={"description": "config name"})

    path_params: PathParams
    response: Optional[V1alpha2GenericPlatformConfiguration] = field(
        default=V1alpha2GenericPlatformConfiguration
    )
    endpoint_id: Optional[str] = field(default="patchPlatformConfiguration")


@define(kw_only=True)
@router.put("/kapis/config.kubesphere.io/v1alpha2/platformconfigs/{config}")
class UpdatePlatformConfigurationAPI(BaseAPI[V1alpha2GenericPlatformConfiguration]):
    """Allows the user to modify the configuration settings of the specified platform"""

    @define
    class PathParams:
        config: str = field(metadata={"description": "config name"})

    @define
    class RequestBodyModel:
        apiVersion: Optional[str] = field(
            default=None,
            metadata={
                "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
            },
        )
        data: Optional[Any] = field(default=None)
        kind: Optional[str] = field(
            default=None,
            metadata={
                "description": "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
            },
        )
        metadata: Optional[V1ObjectMeta] = field(default=None)

    request_body: RequestBodyModel

    path_params: PathParams
    response: Optional[V1alpha2GenericPlatformConfiguration] = field(
        default=V1alpha2GenericPlatformConfiguration
    )
    endpoint_id: Optional[str] = field(default="updatePlatformConfiguration")


@define(kw_only=True)
@router.get(
    "/kapis/gateway.kubesphere.io/v1alpha2/namespaces/{namespace}/availableingressclassscopes"
)
class ListIngressClassScopesAPI(BaseAPI[V1alpha2IngressClassScope]):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "The specified namespace."})

    path_params: PathParams
    response: Optional[V1alpha2IngressClassScope] = field(
        default=V1alpha2IngressClassScope
    )
    endpoint_id: Optional[str] = field(default="ListIngressClassScopes")


@define(kw_only=True)
@router.get("/kapis/package.kubesphere.io/v1alpha1/extensionversions/{version}/files")
class ListExtensionVersionFilesAPI(BaseAPI[LoaderBufferedFile]):
    """None"""

    @define
    class PathParams:
        version: str = field(
            metadata={"description": "The specified extension version name."}
        )

    path_params: PathParams
    response: Optional[LoaderBufferedFile] = field(default=LoaderBufferedFile)
    endpoint_id: Optional[str] = field(default="list-extension-version-files")


@define(kw_only=True)
@router.post("/static/images")
class UploadImageAPI(BaseAPI):
    """None"""

    @define
    class RequestBodyModel:
        image: Optional[str] = field(default=None)

    request_body: RequestBodyModel

    endpoint_id: Optional[str] = field(default="uploadImage")


@define(kw_only=True)
@router.get("/static/images/{file}")
class GetImageAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        file: str = field(metadata={"description": "File name of the image."})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="getImage")
