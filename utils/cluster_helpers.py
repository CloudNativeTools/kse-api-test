# -*- coding:utf-8 -*-
"""
集群相关公共函数
"""
from apis.ks_core.user_related_resources.apis import (
    ListClustersAPI,
    CreateWorkspaceTemplateAPI,
    DeleteWorkspaceTemplateAPI,
    CreateNamespaceAPI,
    DeleteNamespaceAPI,
)
from apis.ks_core.user_related_resources.models import (
    V1beta1WorkspaceTemplateSpec,
    V1beta1GenericPlacement,
    V1beta1GenericClusterReference,
    V1beta1Template,
    V1beta1ObjectMeta,
    V1beta1WorkspaceSpec,
)
from aomaker.storage import cache


def get_clusters():
    """
    获取集群列表

    Returns:
        tuple: (host_cluster_name, member_cluster_name)
            - host_cluster_name: 必有，host集群名称
            - member_cluster_name: 可选，member集群名称（没有则为None）

    Example:
        host_cluster, member_cluster = get_clusters()
        if not host_cluster:
            pytest.skip("无host集群")
    """
    api = ListClustersAPI()
    res = api.send()

    if res.cached_response.raw_response.status_code == 200:
        data = res.cached_response.raw_response.json()
        clusters = data.get("items", [])

        host_cluster = None
        member_cluster = None

        for c in clusters:
            labels = c.get("metadata", {}).get("labels", {})
            if labels.get("cluster-role.kubesphere.io/host"):
                host_cluster = c["metadata"]["name"]
            else:
                if member_cluster is None:
                    member_cluster = c["metadata"]["name"]

        return host_cluster, member_cluster

    return None, None


def set_current_cluster(cluster_name: str):
    """
    设置当前集群名称到缓存
    
    中间件会自动为资源类接口添加 /clusters/{cluster} 前缀
    
    Args:
        cluster_name: 集群名称
        
    Example:
        host_cluster, _ = get_clusters()
        set_current_cluster(host_cluster)  # 后续请求会自动添加 /clusters/{host_cluster} 前缀
    """
    cache.set("current_cluster", cluster_name)


def clear_current_cluster():
    """
    清除当前集群设置
    
    Example:
        clear_current_cluster()  # 清除后不再自动添加集群前缀
    """
    cache.delete("current_cluster")


def setup_test_workspace_and_project():
    """
    创建测试企业空间和项目

    Host集群：创建企业空间 ws-host-test 和项目 host-pro1-test
    Member集群（如有）：创建企业空间 ws-member-test 和项目 mem-pro1-test

    Returns:
        tuple: (success, host_cluster, member_cluster)
            - success: bool，是否创建成功
            - host_cluster: host集群名称
            - member_cluster: member集群名称（可能为None）

    Example:
        success, host_cluster, member_cluster = setup_test_workspace_and_project()
        if not success:
            pytest.skip("无法创建测试数据")
    """
    host_cluster, member_cluster = get_clusters()

    if not host_cluster:
        return False, None, None

    # Host集群：创建企业空间和项目
    # 创建企业空间（使用WorkspaceTemplate，指定placement.clusters）
    placement = V1beta1GenericPlacement(
        clusters=[V1beta1GenericClusterReference(name=host_cluster)]
    )
    template = V1beta1Template(
        metadata=V1beta1ObjectMeta(annotations={"kubesphere.io/creator": "admin"}),
        spec=V1beta1WorkspaceSpec(manager="admin")
    )
    spec = V1beta1WorkspaceTemplateSpec(placement=placement, template=template)

    ws_api = CreateWorkspaceTemplateAPI(request_body={
        "apiVersion": "iam.kubesphere.io/v1beta1",
        "kind": "WorkspaceTemplate",
        "metadata": {
            "name": "ws-host-test",
            "annotations": {"kubesphere.io/creator": "admin"}
        },
        "spec": spec
    })
    ws_api.send()

    # 创建项目（设置当前集群，中间件会自动添加 /clusters/xxx 前缀）
    set_current_cluster(host_cluster)
    try:
        path_params = CreateNamespaceAPI.PathParams(workspace="ws-host-test")
        ns_api = CreateNamespaceAPI(
            path_params=path_params,
            request_body={
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": {
                    "name": "host-pro1-test",
                    "labels": {
                        "kubesphere.io/workspace": "ws-host-test",
                        "kubesphere.io/managed": "true"
                    },
                    "annotations": {"kubesphere.io/creator": "admin"}
                }
            }
        )
        ns_api.send()
    finally:
        clear_current_cluster()

    # Member集群（如有）：创建企业空间和项目
    if member_cluster:
        # 创建企业空间
        placement = V1beta1GenericPlacement(
            clusters=[V1beta1GenericClusterReference(name=member_cluster)]
        )
        template = V1beta1Template(
            metadata=V1beta1ObjectMeta(annotations={"kubesphere.io/creator": "admin"}),
            spec=V1beta1WorkspaceSpec(manager="admin")
        )
        spec = V1beta1WorkspaceTemplateSpec(placement=placement, template=template)

        ws_api = CreateWorkspaceTemplateAPI(request_body={
            "apiVersion": "iam.kubesphere.io/v1beta1",
            "kind": "WorkspaceTemplate",
            "metadata": {
                "name": "ws-member-test",
                "annotations": {"kubesphere.io/creator": "admin"}
            },
            "spec": spec
        })
        ws_api.send()

        # 创建项目（设置当前集群，中间件会自动添加 /clusters/xxx 前缀）
        set_current_cluster(member_cluster)
        try:
            path_params = CreateNamespaceAPI.PathParams(workspace="ws-member-test")
            ns_api = CreateNamespaceAPI(
                path_params=path_params,
                request_body={
                    "apiVersion": "v1",
                    "kind": "Namespace",
                    "metadata": {
                        "name": "mem-pro1-test",
                        "labels": {
                            "kubesphere.io/workspace": "ws-member-test",
                            "kubesphere.io/managed": "true"
                        },
                        "annotations": {"kubesphere.io/creator": "admin"}
                    }
                }
            )
            ns_api.send()
        finally:
            clear_current_cluster()

    return True, host_cluster, member_cluster


def cleanup_test_workspace_and_project():
    """
    清理测试创建的企业空间和项目

    删除Host集群的：ws-host-test 企业空间和 host-pro1-test 项目
    删除Member集群的（如有）：ws-member-test 企业空间和 mem-pro1-test 项目

    Returns:
        bool: 是否执行完成（无论资源是否存在都返回True）

    Example:
        # 在测试结束时调用
        cleanup_test_workspace_and_project()
    """
    host_cluster, member_cluster = get_clusters()

    if not host_cluster:
        return True

    # Host集群：删除项目和企业空间（先删项目，再删企业空间）
    # 删除项目（设置当前集群，中间件会自动添加 /clusters/xxx 前缀）
    set_current_cluster(host_cluster)
    try:
        path_params = DeleteNamespaceAPI.PathParams(
            workspace="ws-host-test",
            namespace="host-pro1-test"
        )
        DeleteNamespaceAPI(path_params=path_params).send()
    except Exception:
        pass  # 资源可能不存在，忽略错误
    finally:
        clear_current_cluster()

    # 删除企业空间
    try:
        path_params = DeleteWorkspaceTemplateAPI.PathParams(workspace="ws-host-test")
        delete_ws_api = DeleteWorkspaceTemplateAPI(
            path_params=path_params,
            request_body={
                "kind": "DeleteOptions",
                "apiVersion": "v1",
                "propagationPolicy": "Orphan"
            }
        )
        delete_ws_api.send()
    except Exception:
        pass  # 资源可能不存在，忽略错误

    # Member集群（如有）：删除项目和企业空间
    if member_cluster:
        # 删除项目（设置当前集群，中间件会自动添加 /clusters/xxx 前缀）
        set_current_cluster(member_cluster)
        try:
            path_params = DeleteNamespaceAPI.PathParams(
                workspace="ws-member-test",
                namespace="mem-pro1-test"
            )
            DeleteNamespaceAPI(path_params=path_params).send()
        except Exception:
            pass  # 资源可能不存在，忽略错误
        finally:
            clear_current_cluster()

        # 删除企业空间
        try:
            path_params = DeleteWorkspaceTemplateAPI.PathParams(workspace="ws-member-test")
            delete_ws_api = DeleteWorkspaceTemplateAPI(
                path_params=path_params,
                request_body={
                    "kind": "DeleteOptions",
                    "apiVersion": "v1",
                    "propagationPolicy": "Orphan"
                }
            )
            delete_ws_api.send()
        except Exception:
            pass  # 资源可能不存在，忽略错误

    return True
