from typing import Optional, List
from attrs import define, field
from .models import V1alpha2IngressClassScope, LoaderBufferedFile
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "ListAppRlsAPI",
    "CreateOrUpdateAppRlsAPI",
    "DeleteAppRlsAPI",
    "DescribeAppRlsAPI",
    "CreateOrUpdateAppRlsAPI_1",
    "ListAppsAPI",
    "CreateOrUpdateAppAPI",
    "DeleteAppAPI",
    "DescribeAppAPI",
    "PatchAppAPI",
    "CreateOrUpdateAppAPI_1",
    "DoAppActionAPI",
    "AppCrListAPI",
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
    "CreateOrUpdateCRAPI",
    "DeleteAppCrAPI",
    "DescribeAppCrAPI",
    "ListAppRlsAPI_1",
    "CreateOrUpdateAppRlsAPI_2",
    "DeleteAppRlsAPI_1",
    "DescribeAppRlsAPI_1",
    "CreateOrUpdateAppRlsAPI_3",
    "AppCrListAPI_1",
    "CreateOrUpdateCRAPI_1",
    "DeleteAppCrAPI_1",
    "DescribeAppCrAPI_1",
    "ListReposAPI",
    "CreateOrUpdateRepoAPI",
    "DeleteRepoAPI",
    "DescribeRepoAPI",
    "CreateOrUpdateRepoAPI_1",
    "ListRepoEventsAPI",
    "ListReviewsAPI",
    "ListAppRlsAPI_2",
    "CreateOrUpdateAppRlsAPI_4",
    "ListAppsAPI_1",
    "CreateOrUpdateAppAPI_2",
    "DeleteAppAPI_1",
    "DescribeAppAPI_1",
    "PatchAppAPI_1",
    "CreateOrUpdateAppAPI_3",
    "AppCrListAPI_2",
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
    "CreateOrUpdateCRAPI_2",
    "DeleteAppCrAPI_2",
    "DescribeAppCrAPI_2",
    "ListReposAPI_1",
    "CreateOrUpdateRepoAPI_2",
    "DeleteRepoAPI_1",
    "DescribeRepoAPI_1",
    "CreateOrUpdateRepoAPI_3",
    "ListRepoEventsAPI_1",
    "ListIngressClassScopesAPI",
    "ListExtensionVersionFilesAPI",
    "UploadImageAPI",
    "GetImageAPI",
]


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/applications")
class ListAppRlsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="ListAppRls")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/applications")
class CreateOrUpdateAppRlsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/applications/{application}")
class DeleteAppRlsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DeleteAppRls")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/applications/{application}")
class DescribeAppRlsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DescribeAppRls")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/applications/{application}")
class CreateOrUpdateAppRlsAPI_1(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps")
class ListAppsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="ListApps")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps")
class CreateOrUpdateAppAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateApp")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/apps/{app}")
class DeleteAppAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DeleteApp")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}")
class DescribeAppAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DescribeApp")


@define(kw_only=True)
@router.patch("/kapis/application.kubesphere.io/v2/apps/{app}")
class PatchAppAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="PatchApp")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}")
class CreateOrUpdateAppAPI_1(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateApp")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}/action")
class DoAppActionAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DoAppAction")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/cr")
class AppCrListAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="AppCrList")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/examplecr/{name}")
class ExampleCrAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="exampleCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/versions")
class ListAppVersionsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="ListAppVersions")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}/versions")
class CreateOrUpdateAppVersionAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppVersion")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}")
class DeleteAppVersionAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DeleteAppVersion")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}")
class DescribeAppVersionAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DescribeAppVersion")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}")
class CreateOrUpdateAppVersionAPI_1(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppVersion")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/apps/{app}/versions/{version}/action")
class AppVersionActionAPI(BaseAPI):
    """None"""

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
class CreateAttachmentAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateAttachment")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/attachments/{attachment}")
class DeleteAttachmentsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DeleteAttachments")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/attachments/{attachment}")
class DescribeAttachmentAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DescribeAttachment")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/categories")
class ListCategoriesAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="ListCategories")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/categories")
class CreateOrUpdateCategoryAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateCategory")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/categories/{category}")
class DeleteCategoryAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DeleteCategory")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/categories/{category}")
class DescribeCategoryAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DescribeCategory")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/categories/{category}")
class CreateOrUpdateCategoryAPI_1(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateCategory")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/cr")
class CreateOrUpdateCRAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateCR")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/cr/{crname}")
class DeleteAppCrAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DeleteAppCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/cr/{crname}")
class DescribeAppCrAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DescribeAppCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications")
class ListAppRlsAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="ListAppRls")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications")
class CreateOrUpdateAppRlsAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}"
)
class DeleteAppRlsAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DeleteAppRls")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}"
)
class DescribeAppRlsAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DescribeAppRls")


@define(kw_only=True)
@router.post(
    "/kapis/application.kubesphere.io/v2/namespaces/{namespace}/applications/{application}"
)
class CreateOrUpdateAppRlsAPI_3(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/namespaces/{namespace}/apps/{app}/cr")
class AppCrListAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="AppCrList")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/namespaces/{namespace}/cr")
class CreateOrUpdateCRAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateCR")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/namespaces/{namespace}/cr/{crname}")
class DeleteAppCrAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DeleteAppCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/namespaces/{namespace}/cr/{crname}")
class DescribeAppCrAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        namespace: str = field(metadata={"description": "namespace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DescribeAppCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/repos")
class ListReposAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="ListRepos")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/repos")
class CreateOrUpdateRepoAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateRepo")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/repos/{repo}")
class DeleteRepoAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DeleteRepo")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/repos/{repo}")
class DescribeRepoAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="DescribeRepo")


@define(kw_only=True)
@router.patch("/kapis/application.kubesphere.io/v2/repos/{repo}")
class CreateOrUpdateRepoAPI_1(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="CreateOrUpdateRepo")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/repos/{repo}/events")
class ListRepoEventsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="ListRepoEvents")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/reviews")
class ListReviewsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="ListReviews")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/applications")
class ListAppRlsAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="ListAppRls")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/applications")
class CreateOrUpdateAppRlsAPI_4(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateAppRls")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps")
class ListAppsAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
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
class DeleteAppAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DeleteApp")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}")
class DescribeAppAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DescribeApp")


@define(kw_only=True)
@router.patch("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}")
class PatchAppAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
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
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/cr")
class AppCrListAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="AppCrList")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/examplecr/{name}"
)
class ExampleCrAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="exampleCr")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions"
)
class ListAppVersionsAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
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
class DeleteAppVersionAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DeleteAppVersion")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/apps/{app}/versions/{version}"
)
class DescribeAppVersionAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
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
class AppVersionActionAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
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
class CreateAttachmentAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateAttachment")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/attachments/{attachment}"
)
class DeleteAttachmentsAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DeleteAttachments")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/attachments/{attachment}"
)
class DescribeAttachmentAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DescribeAttachment")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/cr")
class CreateOrUpdateCRAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateCR")


@define(kw_only=True)
@router.delete("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/cr/{crname}")
class DeleteAppCrAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DeleteAppCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/cr/{crname}")
class DescribeAppCrAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DescribeAppCr")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos")
class ListReposAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="ListRepos")


@define(kw_only=True)
@router.post("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos")
class CreateOrUpdateRepoAPI_2(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateRepo")


@define(kw_only=True)
@router.delete(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}"
)
class DeleteRepoAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DeleteRepo")


@define(kw_only=True)
@router.get("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}")
class DescribeRepoAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="DescribeRepo")


@define(kw_only=True)
@router.patch("/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}")
class CreateOrUpdateRepoAPI_3(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="CreateOrUpdateRepo")


@define(kw_only=True)
@router.get(
    "/kapis/application.kubesphere.io/v2/workspaces/{workspace}/repos/{repo}/events"
)
class ListRepoEventsAPI_1(BaseAPI):
    """None"""

    @define
    class PathParams:
        workspace: str = field(metadata={"description": "workspace"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="ListRepoEvents")


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
