# -*- coding:utf-8 -*-
"""
集群相关公共函数
"""
import time
from apis.ks_core.user_related_resources.apis import (
    ListClustersAPI,
    CreateWorkspaceTemplateAPI,
    CreateNamespaceAPI,
    ListNamespacesWorkspaceAPI,
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
from utils.test_data_helper import load_test_data, _get_nested_value


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
    # 获取 host 集群标签（使用 replace_vars=False 避免变量替换）
    host_label = 'cluster-role.kubesphere.io/host'
    
    max_retries = 3
    last_error = None
    
    for attempt in range(max_retries):
        try:
            api = ListClustersAPI()
            res = api.send()

            if res.cached_response.raw_response.status_code == 200:
                data = res.cached_response.raw_response.json()
                clusters = data.get("items", [])

                host_cluster = None
                member_cluster = None
                
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

                # 不再缓存到数据库，直接返回
                return host_cluster, member_cluster
            
            break  # 成功或非 200 状态码，退出重试循环
            
        except Exception as e:
            last_error = e
            if "database is locked" in str(e) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 0.5
                print(f"  ⚠️ 获取集群列表遇到数据库锁定，等待 {wait_time}s 后重试...")
                time.sleep(wait_time)
                continue
            raise
    
    if last_error:
        raise last_error
    
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
    cache.upsert("current_cluster", cluster_name)


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
    # 加载配置（先不替换变量，避免触发 cache 访问）
    config_raw = load_test_data('ks_core', 'test_environment', default={}, replace_vars=False)
    if not config_raw:
        print("⚠️ 警告: 无法加载测试环境配置")
        print(f"  尝试的文件路径: data/api_data/ks_core/test_environment.json")
        return False, {}

    # 直接获取集群信息（不在 cache 中存储）
    host_cluster, member_cluster = get_clusters()

    if not host_cluster:
        return False, config_raw

    # 确保 creator 和 manager 是字符串（如果是列表，取第一个元素）
    def get_string_value(value):
        if isinstance(value, list):
            return value[0] if value else 'admin'
        return str(value) if value else 'admin'
    
    # 从 test_users 配置中获取 admin 用户名
    try:
        admin_username = _get_nested_value('test_users', 'admin', 'username')
    except Exception:
        admin_username = 'admin'
    
    # 使用 admin 用户名替换配置中的变量
    host_ws = config_raw.get('workspaces', {}).get('host', {})
    host_ws_creator = host_ws.get('creator', 'admin')
    host_ws_manager = host_ws.get('manager', 'admin')
    host_creator = get_string_value(host_ws_creator)
    host_manager = get_string_value(host_ws_manager)
    
    # 如果是变量占位符，替换为实际值
    if '{{' in host_creator:
        host_creator = admin_username
    if '{{' in host_manager:
        host_manager = admin_username
    
    host_proj = config_raw.get('projects', {}).get('host', {})
    
    print(f"✓ Host 企业空间信息:")
    print(f"  - 名称: {host_ws.get('name', 'ws-host-test')}")
    print(f"  - 创建者: {host_creator}")
    print(f"  - 管理员: {host_manager}")
    
    try:
        _create_workspace_and_project(
            cluster=host_cluster,
            workspace_name=host_ws.get('name', 'ws-host-test'),
            workspace_alias=host_ws.get('alias', 'Host测试企业空间'),
            project_name=host_proj.get('name', 'host-pro1-test'),
            project_alias=host_proj.get('alias', 'Host测试项目'),
            creator=host_creator,
            manager=host_manager,
        )
    except Exception as e:
        print(f"⚠️ 警告: Host 企业空间或项目创建失败: {e}")
        import traceback
        traceback.print_exc()

    # Member集群（如有）：创建企业空间和项目
    member_ws = config_raw.get('workspaces', {}).get('member', {})
    member_proj = config_raw.get('projects', {}).get('member', {})
    
    if member_cluster and member_ws:
        member_ws_creator = member_ws.get('creator', 'admin')
        member_ws_manager = member_ws.get('manager', 'admin')
        member_creator = get_string_value(member_ws_creator)
        member_manager = get_string_value(member_ws_manager)
        
        # 如果是变量占位符，替换为实际值
        if '{{' in member_creator:
            member_creator = admin_username
        if '{{' in member_manager:
            member_manager = admin_username
        
        print(f"✓ Member 企业空间信息:")
        print(f"  - 名称: {member_ws.get('name', 'ws-member-test')}")
        print(f"  - 创建者: {member_creator}")
        print(f"  - 管理员: {member_manager}")
        
        try:
            _create_workspace_and_project(
                cluster=member_cluster,
                workspace_name=member_ws.get('name', 'ws-member-test'),
                workspace_alias=member_ws.get('alias', 'Member测试企业空间'),
                project_name=member_proj.get('name', 'mem-pro1-test'),
                project_alias=member_proj.get('alias', 'Member测试项目'),
                creator=member_creator,
                manager=member_manager,
            )
        except Exception as e:
            print(f"⚠️ 警告: Member 企业空间或项目创建失败: {e}")
            import traceback
            traceback.print_exc()

    return True, config_raw


def _create_workspace_and_project(
    cluster: str,
    workspace_name: str,
    workspace_alias: str,
    project_name: str,
    project_alias: str,
    creator: str = "admin",
    manager: str = "admin",
    max_retries: int = 5,
):
    """
    在指定集群创建企业空间和项目（内部方法）
    
    幂等性处理：
    - 如果企业空间已存在，跳过创建
    - 如果项目已存在，跳过创建

    Args:
        cluster: 集群名称
        workspace_name: 企业空间名称
        workspace_alias: 企业空间别名
        project_name: 项目名称
        project_alias: 项目别名
        creator: 创建者
        manager: 管理员
        max_retries: 最大重试次数
    """
    # 加载公共配置
    cluster_config = load_test_data('_common', 'cluster_config', default={}, replace_vars=False)
    default_creator = cluster_config.get('default_creator', 'admin')
    creator = creator or default_creator
    
    ks_core_common = load_test_data('ks_core', '_common', default={}, replace_vars=False)
    api_version = ks_core_common.get('api_versions', {}).get('workspace_template', 'iam.kubesphere.io/v1beta1')
    kind = ks_core_common.get('kinds', {}).get('workspace_template', 'WorkspaceTemplate')

    print(f"  → 尝试创建企业空间 {workspace_name}...")

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

    ws_api = CreateWorkspaceTemplateAPI(
        request_body={
            "apiVersion": api_version,
            "kind": kind,
            "metadata": {
                "name": workspace_name,
                "annotations": {"kubesphere.io/creator": creator}
            },
            "spec": spec
        },
        enable_schema_validation=False
    )

    ws_created = False
    for attempt in range(max_retries):
        try:
            ws_api.send()
            ws_created = True
            print(f"  ✓ 企业空间 {workspace_name} 创建成功")
            break
        except Exception as e:
            error_msg = str(e)
            if "database is locked" in error_msg and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 1.0
                print(f"  ⚠️ 企业空间创建遇到数据库锁定，等待 {wait_time}s 后重试...")
                time.sleep(wait_time)
                continue
            if "409" in error_msg or "already exists" in error_msg.lower():
                print(f"  ✓ 企业空间 {workspace_name} 已存在，可复用")
                break
            raise

    print(f"  ⏳ 等待 1s 确保企业空间 {workspace_name} 完全创建...")
    time.sleep(1.0)

    ns_exists = False
    set_current_cluster(cluster)
    try:
        list_ns_api = ListNamespacesWorkspaceAPI(
            path_params=ListNamespacesWorkspaceAPI.PathParams(workspace=workspace_name),
            enable_schema_validation=False
        )
        res = list_ns_api.send()
        if res.cached_response.raw_response.status_code == 200:
            data = res.cached_response.raw_response.json()
            namespaces = data.get('items', [])
            ns_exists = any(ns.get('metadata', {}).get('name') == project_name for ns in namespaces)
            if ns_exists:
                print(f"  ✓ 项目 {project_name} 已存在，可复用")
            else:
                print(f"  ⚠️ 项目 {project_name} 不存在，将创建")
    except Exception as e:
        print(f"  ⚠️ 查询项目列表失败: {e}，将尝试创建")
    finally:
        clear_current_cluster()

    if not ns_exists:
        set_current_cluster(cluster)
        try:
            path_params = CreateNamespaceAPI.PathParams(workspace=workspace_name)

            request_body = {
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

            if "member" in cluster.lower():
                request_body["placement"] = {
                    "clusters": [{"name": cluster}]
                }

            ns_api = CreateNamespaceAPI(
                path_params=path_params,
                request_body=request_body,
                enable_schema_validation=False
            )

            for attempt in range(max_retries):
                try:
                    ns_api.send()
                    print(f"  ✓ 项目 {project_name} 创建成功")
                    break
                except Exception as e:
                    error_msg = str(e)
                    if "database is locked" in error_msg and attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 1.0
                        print(f"  ⚠️ 项目创建遇到数据库锁定，等待 {wait_time}s 后重试...")
                        time.sleep(wait_time)
                        continue
                    raise
        finally:
            clear_current_cluster()


def cleanup_test_environment():
    """
    清理测试环境
    
    注意：不再清理资源，保留测试数据供后续使用。
    资源会持续存在，直到手动删除或下次运行时覆盖。

    Returns:
        tuple: (success, config)
            - success: bool，是否执行完成
            - config: dict，测试环境配置
    """
    print("  ℹ️ 跳过清理，保留测试数据供后续使用")
    config = load_test_data('ks_core', 'test_environment', default={}, replace_vars=False)
    return True, config


def _delete_workspace_and_project(
    cluster: str,
    workspace_name: str,
    project_name: str,
):
    """
    在指定集群删除企业空间和项目（内部方法）
    
    注意：此函数已禁用，不再执行删除操作。

    Args:
        cluster: 集群名称
        workspace_name: 企业空间名称
        project_name: 项目名称
    """
    # 不再执行删除操作，保留资源
    pass



