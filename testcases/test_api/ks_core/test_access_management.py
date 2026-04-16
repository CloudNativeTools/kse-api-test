# -*- coding:utf-8 -*-
import pytest

from apis.ks_core.access_management.apis import (
    ListClusterMembersAPI,
    CreateClusterMembersAPI,
    RemoveClusterMemberAPI,
    UpdateClusterMemberAPI,
    ListNamespaceMembersAPI,
    CreateSubjectAccessReviewAPI,
    ListRoleTemplateOfUserAPI,
    ListWorkspaceMembersAPI
)
from apis.ks_core.access_management.models import (
    V1beta1SubjectAccessReviewSpec,
    V1beta1ResourceAttributes
)
from utils.test_data_helper import get_test_data_list


INVALID_MEMBERS = get_test_data_list("ks_core", "access_management/members", "invalid_members")


@pytest.mark.access_management
def test_list_cluster_members_success():
    """获取集群成员列表"""
    res = ListClusterMembersAPI().send()
    assert res.cached_response.raw_response.status_code == 200

    data = res.cached_response.raw_response.json()
    assert "items" in data and "totalItems" in data
    assert isinstance(data["items"], list)


@pytest.mark.access_management
def test_list_cluster_members_with_role_filter():
    """按角色过滤集群成员"""
    api = ListClusterMembersAPI()
    api.query_params.clusterrole = "cluster-admin"
    res = api.send()
    assert res.cached_response.raw_response.status_code == 200


@pytest.mark.access_management
def test_list_namespace_members_success():
    """获取命名空间成员列表"""
    path_params = ListNamespaceMembersAPI.PathParams(namespace="default")
    res = ListNamespaceMembersAPI(path_params=path_params).send()
    assert res.cached_response.raw_response.status_code == 200

    data = res.cached_response.raw_response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


@pytest.mark.access_management
def test_list_workspace_members_success():
    """获取工作空间成员列表"""
    path_params = ListWorkspaceMembersAPI.PathParams(workspace="system-workspace")
    res = ListWorkspaceMembersAPI(path_params=path_params).send()
    assert res.cached_response.raw_response.status_code == 200

    data = res.cached_response.raw_response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


@pytest.mark.access_management
def test_list_role_templates_of_user():
    """获取用户角色模板"""
    path_params = ListRoleTemplateOfUserAPI.PathParams(username="admin")
    res = ListRoleTemplateOfUserAPI(path_params=path_params).send()
    assert res.cached_response.raw_response.status_code == 200

    data = res.cached_response.raw_response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


@pytest.mark.access_management
def test_create_subject_access_review_success():
    """创建权限审查请求"""
    resource_attrs = V1beta1ResourceAttributes(
        resource="pods",
        verb="get",
        namespace="default"
    )
    spec = V1beta1SubjectAccessReviewSpec(
        user="admin",
        resourceAttributes=resource_attrs
    )
    request_body = CreateSubjectAccessReviewAPI.RequestBodyModel(
        spec=spec,
        apiVersion="authorization.k8s.io/v1beta1",
        kind="SubjectAccessReview"
    )
    res = CreateSubjectAccessReviewAPI(request_body=request_body).send()
    assert res.cached_response.raw_response.status_code == 200

    data = res.cached_response.raw_response.json()
    assert "status" in data and "allowed" in data["status"]


@pytest.mark.access_management
@pytest.mark.parametrize("member_data", INVALID_MEMBERS)
def test_create_cluster_members_invalid_data(member_data):
    """创建集群成员-无效角色"""
    api = CreateClusterMembersAPI(request_body=[member_data])
    res = api.send()
    assert res.cached_response.raw_response.status_code >= 400


@pytest.mark.access_management
def test_remove_nonexistent_cluster_member():
    """删除不存在的集群成员"""
    path_params = RemoveClusterMemberAPI.PathParams(clustermember="nonexistent-user")
    res = RemoveClusterMemberAPI(path_params=path_params).send()
    assert res.cached_response.raw_response.status_code == 200


@pytest.mark.access_management
@pytest.mark.parametrize("member_data", INVALID_MEMBERS)
def test_update_cluster_member_invalid_data(member_data):
    """更新集群成员-无效角色"""
    path_params = UpdateClusterMemberAPI.PathParams(clustermember="admin")
    api = UpdateClusterMemberAPI(path_params=path_params, request_body=member_data)
    res = api.send()
    assert res.cached_response.raw_response.status_code >= 400
