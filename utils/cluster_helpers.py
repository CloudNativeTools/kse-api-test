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
from utils.test_data_helper import load_test_data


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
        
        # 从配置中获取 host 集群标签
        cluster_config = load_test_data('_common', 'cluster_config', default={})
        host_label = cluster_config.get('host_cluster_label', 'cluster-role.kubesphere.io/host')
        
        # 调试日志
        if not clusters:
            print("⚠️ 警告: 集群列表为空")

        for c in clusters:
            cluster_name = c.get("metadata", {}).get("name", "unknown")
            labels = c.get("metadata", {}).get("labels", {})
            
            # 检查是否有 host 标签（允许空字符串值）
            has_host_label = host_label in labels
            
            if has_host_label:
                host_cluster = cluster_name
                print(f"✓ 找到 Host 集群: {cluster_name}")
            else:
                if member_cluster is None:
                    member_cluster = cluster_name
                    print(f"✓ 找到 Member 集群: {cluster_name}")

        # 缓存集群信息（使用 try-except 避免 UNIQUE constraint 冲突）
        if host_cluster:
            try:
                cache.set('host_cluster', host_cluster)
            except Exception:
                pass  # 如果已存在就忽略
        if member_cluster:
            try:
                cache.set('member_cluster', member_cluster)
            except Exception:
                pass  # 如果已存在就忽略

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
    try:
        cache.del_by_condition(where={'var_name': 'current_cluster'})
    except Exception:
        pass  # 忽略删除失败


def setup_test_environment():
    """
    创建测试环境（从配置文件加载数据）

    从 /data/api_data/ks_core/test_environment.json 读取配置：
    - Host集群：创建企业空间和项目
    - Member集群（如有）：创建企业空间和项目

    Returns:
        tuple: (success, config)
            - success: bool，是否创建成功
            - config: dict，测试环境配置

    Example:
        success, config = setup_test_environment()
        if not success:
            pytest.skip("无法创建测试数据")
    """
    # 加载配置（自动替换变量）
    config = load_test_data('ks_core', 'test_environment', default={})
    if not config:
        print("⚠️ 警告: 无法加载测试环境配置")
        print(f"  尝试的文件路径: data/api_data/ks_core/test_environment.json")
        return False, {}

    host_cluster, member_cluster = get_clusters()

    if not host_cluster:
        return False, config

    workspaces = config.get('workspaces', {})
    projects = config.get('projects', {})

    # Host集群：创建企业空间和项目
    host_ws = workspaces.get('host', {})
    host_proj = projects.get('host', {})
    
    _create_workspace_and_project(
        cluster=host_cluster,
        workspace_name=host_ws.get('name', 'ws-host-test'),
        workspace_alias=host_ws.get('alias', 'Host测试企业空间'),
        project_name=host_proj.get('name', 'host-pro1-test'),
        project_alias=host_proj.get('alias', 'Host测试项目'),
        creator=host_ws.get('creator', 'admin'),
        manager=host_ws.get('manager', 'admin'),
    )

    # Member集群（如有）：创建企业空间和项目
    if member_cluster:
        member_ws = workspaces.get('member', {})
        member_proj = projects.get('member', {})
        
        _create_workspace_and_project(
            cluster=member_cluster,
            workspace_name=member_ws.get('name', 'ws-member-test'),
            workspace_alias=member_ws.get('alias', 'Member测试企业空间'),
            project_name=member_proj.get('name', 'mem-pro1-test'),
            project_alias=member_proj.get('alias', 'Member测试项目'),
            creator=member_ws.get('creator', 'admin'),
            manager=member_ws.get('manager', 'admin'),
        )

    return True, config


def _create_workspace_and_project(
    cluster: str,
    workspace_name: str,
    workspace_alias: str,
    project_name: str,
    project_alias: str,
    creator: str = "admin",
    manager: str = "admin",
):
    """
    在指定集群创建企业空间和项目（内部方法）

    Args:
        cluster: 集群名称
        workspace_name: 企业空间名称
        workspace_alias: 企业空间别名
        project_name: 项目名称
        project_alias: 项目别名
        creator: 创建者
        manager: 管理员
    """
    # 加载公共配置
    cluster_config = load_test_data('_common', 'cluster_config', default={})
    default_creator = cluster_config.get('default_creator', 'admin')
    creator = creator or default_creator
    
    ks_core_common = load_test_data('ks_core', '_common', default={})
    api_version = ks_core_common.get('api_versions', {}).get('workspace_template', 'iam.kubesphere.io/v1beta1')
    kind = ks_core_common.get('kinds', {}).get('workspace_template', 'WorkspaceTemplate')

    # 创建企业空间（使用WorkspaceTemplate，指定placement.clusters）
    placement = V1beta1GenericPlacement(
        clusters=[V1beta1GenericClusterReference(name=cluster)]
    )
    template = V1beta1Template(
        metadata=V1beta1ObjectMeta(
            annotations={"kubesphere.io/creator": creator},
            labels={"kubesphere.io/workspace-alias": workspace_alias}
        ),
        spec=V1beta1WorkspaceSpec(manager=manager)
    )
    spec = V1beta1WorkspaceTemplateSpec(placement=placement, template=template)

    ws_api = CreateWorkspaceTemplateAPI(request_body={
        "apiVersion": api_version,
        "kind": kind,
        "metadata": {
            "name": workspace_name,
            "annotations": {"kubesphere.io/creator": creator}
        },
        "spec": spec
    })
    ws_api.send()

    # 创建项目（设置当前集群，中间件会自动添加 /clusters/xxx 前缀）
    set_current_cluster(cluster)
    try:
        path_params = CreateNamespaceAPI.PathParams(workspace=workspace_name)
        ns_api = CreateNamespaceAPI(
            path_params=path_params,
            request_body={
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": {
                    "name": project_name,
                    "labels": {
                        "kubesphere.io/workspace": workspace_name,
                        "kubesphere.io/managed": "true"
                    },
                    "annotations": {"kubesphere.io/creator": creator}
                }
            }
        )
        ns_api.send()
    finally:
        clear_current_cluster()


def cleanup_test_environment():
    """
    清理测试环境（从配置文件加载数据）

    从 /data/api_data/ks_core/test_environment.json 读取配置：
    - 删除Host集群的测试企业空间和项目
    - 删除Member集群的测试企业空间和项目（如有）

    Returns:
        tuple: (success, config)
            - success: bool，是否执行完成
            - config: dict，测试环境配置

    Example:
        # 在测试结束时调用
        cleanup_test_environment()
    """
    # 加载配置（自动替换变量）
    config = load_test_data('ks_core', 'test_environment', default={})
    if not config:
        return True, {}

    host_cluster, member_cluster = get_clusters()

    if not host_cluster:
        return True, config

    workspaces = config.get('workspaces', {})
    projects = config.get('projects', {})

    # Host集群：删除项目和企业空间（先删项目，再删企业空间）
    host_ws = workspaces.get('host', {})
    host_proj = projects.get('host', {})
    
    _delete_workspace_and_project(
        cluster=host_cluster,
        workspace_name=host_ws.get('name', 'ws-host-test'),
        project_name=host_proj.get('name', 'host-pro1-test'),
    )

    # Member集群（如有）：删除项目和企业空间
    if member_cluster:
        member_ws = workspaces.get('member', {})
        member_proj = projects.get('member', {})
        
        _delete_workspace_and_project(
            cluster=member_cluster,
            workspace_name=member_ws.get('name', 'ws-member-test'),
            project_name=member_proj.get('name', 'mem-pro1-test'),
        )

    return True, config


def _delete_workspace_and_project(
    cluster: str,
    workspace_name: str,
    project_name: str,
):
    """
    在指定集群删除企业空间和项目（内部方法）

    Args:
        cluster: 集群名称
        workspace_name: 企业空间名称
        project_name: 项目名称
    """
    # 删除项目（设置当前集群，中间件会自动添加 /clusters/xxx 前缀）
    set_current_cluster(cluster)
    try:
        path_params = DeleteNamespaceAPI.PathParams(
            workspace=workspace_name,
            namespace=project_name
        )
        DeleteNamespaceAPI(path_params=path_params).send()
    except Exception:
        pass  # 资源可能不存在，忽略错误
    finally:
        clear_current_cluster()

    # 删除企业空间
    try:
        path_params = DeleteWorkspaceTemplateAPI.PathParams(workspace=workspace_name)
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



