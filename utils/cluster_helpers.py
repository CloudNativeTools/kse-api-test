# -*- coding:utf-8 -*-
"""
集群相关公共函数
"""
from loguru import logger
import time
from apis.ks_core.user_related_resources.apis import (
    ListClustersAPI,
    ListWorkspaceTemplatesAPI_1,
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
                    logger.info("未找到任何集群")

                for c in clusters:
                    cluster_name = c.get("metadata", {}).get("name", "unknown")
                    labels = c.get("metadata", {}).get("labels", {})
                    
                    # 检查是否有 host 标签（允许空字符串值）
                    has_host_label = host_label in labels
                    
                    if has_host_label:
                        host_cluster = cluster_name
                        logger.info(f"找到 Host 集群: {cluster_name}")
                    else:
                        if member_cluster is None:
                            member_cluster = cluster_name
                            logger.info(f"找到 Member 集群: {cluster_name}")

                # 不再缓存到数据库，直接返回
                return host_cluster, member_cluster
            
            break  # 成功或非 200 状态码，退出重试循环
            
        except Exception as e:
            last_error = e
            if "database is locked" in str(e) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 0.5
                logger.warning(f"获取集群列表遇到数据库锁定，等待 {wait_time}s 后重试...")
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
        logger.warning(f"无法加载测试环境配置，尝试的文件路径: data/api_data/ks_core/test_environment.json")
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
    
    logger.info(f"Host 企业空间信息: 名称={host_ws.get('name', 'ws-host-test')}, 创建者={host_creator}, 管理员={host_manager}")
    logger.info(f"  创建者: {host_creator}")
    logger.info(f"  管理员: {host_manager}")

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
        logger.warning(f"Host 企业空间/项目创建失败: {e}")
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
        
        logger.info(f"Member 企业空间信息: 名称={member_ws.get('name', 'ws-member-test')}, 创建者={member_creator}, 管理员={member_manager}")
        logger.info(f"  创建者: {member_creator}")
        logger.info(f"  管理员: {member_manager}")
        
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
            logger.info(f"尝试创建企业空间 {workspace_name}...")
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

    # 先查询企业空间是否已存在
    ws_exists = False
    try:
        list_ws_api = ListWorkspaceTemplatesAPI_1(
            query_params=ListWorkspaceTemplatesAPI_1.QueryParams(
                sortBy="createTime",
                limit="10",
                page="1",
            ),
            enable_schema_validation=False
        )
        res = list_ws_api.send()
        if res.cached_response.raw_response.status_code == 200:
            data = res.cached_response.raw_response.json()
            ws_items = data.get('items', [])
            ws_exists = any(ws.get('metadata', {}).get('name') == workspace_name for ws in ws_items)
    except Exception as e:
        logger.warning(f"查询企业空间列表失败: {e}，将尝试直接创建")

    if ws_exists:
        logger.info(f"企业空间 {workspace_name} 已存在，跳过创建")
    else:
        logger.info(f"尝试创建企业空间 {workspace_name}...")

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

        for attempt in range(max_retries):
            try:
                ws_api.send()
                logger.info(f"企业空间 {workspace_name} 创建成功")
                break
            except Exception as e:
                error_msg = str(e)
                if "database is locked" in error_msg and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 1.0
                    logger.warning(f"企业空间创建遇到数据库锁定，等待 {wait_time}s 后重试...")
                    time.sleep(wait_time)
                    continue
                if "409" in error_msg or "already exists" in error_msg.lower():
                    logger.info(f"企业空间 {workspace_name} 已存在，可复用")
                    break
                raise

        logger.info(f"等待 1s 确保企业空间 {workspace_name} 完全创建...")
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
            logger.info(f"项目 {project_name} 已存在，跳过创建")
        else:
            logger.info(f"项目 {project_name} 不存在，将创建")
    except Exception as e:
        logger.warning(f"查询项目列表失败: {e}，将尝试创建")
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
                    logger.info(f"项目 {project_name} 创建成功")
                    break
                except Exception as e:
                    error_msg = str(e)
                    if "database is locked" in error_msg and attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 1.0
                        logger.warning(f"项目创建遇到数据库锁定，等待 {wait_time}s 后重试...")
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
    logger.info("跳过清理，保留测试数据供后续使用")
    config = load_test_data('ks_core', 'test_environment', default={}, replace_vars=False)
    return True, config


def setup_test_users():
    """
    创建测试用户并分配角色（在 setup_test_environment 之后调用）

    用户创建顺序：
    1. 平台级用户（pl-admin, pl-self, pl-regular）- 通过 globalRole 设置
    2. 集群用户（cluster-admin, cluster-viewer）- 创建后邀请加入 host 集群
    3. 企业空间用户（ws-admin, ws-viewer）- 创建后邀请加入 ws-host-test
    4. 项目用户（pro-admin, pro-operator, pro-viewer）- 创建后先加入 ws-host-test，再加入项目

    Returns:
        bool: 是否全部成功
    """
    from apis.ks_core.identity_management.apis import (
        CreateUserAPI,
        ListUsersAPI,
    )
    from apis.ks_core.access_management.apis import (
        CreateClusterMembersAPI,
        CreateWorkspaceMembersAPI,
        CreateNamespaceMembersAPI,
        ListClusterMembersAPI,
        ListWorkspaceMembersAPI,
        ListNamespaceMembersAPI,
    )
    from apis.ks_core.access_management.models import V1beta1Member

    config_raw = load_test_data('ks_core', 'test_environment', default={}, replace_vars=False)
    users_config = config_raw.get('users', {})
    if not users_config:
        logger.warning("未找到用户配置")
        return True

    try:
        admin_username = _get_nested_value('test_users', 'admin', 'username')
    except Exception:
        admin_username = 'admin'

    workspace_name = 'ws-host-test'
    project_name = 'host-pro1-test'

    logger.info("开始创建测试用户...")

    # 预查全部已存在用户，避免逐个 list
    existing_users = set()
    try:
        api = ListUsersAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.page = "1"
        api.query_params.limit = "-1"
        api.query_params.sortBy = "createTime"
        
        res = api.send()
        if res.cached_response.raw_response.status_code == 200:
            data = res.cached_response.raw_response.json()
            existing_users = {u.get('metadata', {}).get('name') for u in data.get('items', [])}
    except Exception as e:
        logger.warning(f"查询已有用户列表失败: {e}")

    def _create_user(username: str, email: str, password: str, global_role: str = None) -> bool:
        if username in existing_users:
            logger.info(f"用户 {username} 已存在，跳过创建")
            return True
        try:
            annotations = {
                "iam.kubesphere.io/uninitialized": "true",
                "kubesphere.io/creator": admin_username
            }
            if global_role:
                annotations["iam.kubesphere.io/globalrole"] = global_role

            request_body = {
                "apiVersion": "iam.kubesphere.io/v1beta1",
                "kind": "User",
                "metadata": {
                    "annotations": annotations,
                    "name": username
                },
                "spec": {
                    "email": email,
                    "password": password
                }
            }

            api = CreateUserAPI(
                request_body=request_body,
                enable_schema_validation=False,
                response=None
            )
            res = api.send()
            if res.cached_response.raw_response.status_code in (200, 201):
                logger.info(f"用户 {username} 创建成功")
                existing_users.add(username)
                return True
            else:
                logger.warning(f"用户 {username} 创建失败: {res.cached_response.raw_response.status_code}")
                return False
        except Exception as e:
            if "already exists" in str(e).lower():
                logger.info(f"用户 {username} 已存在")
                existing_users.add(username)
                return True
            logger.warning(f"用户 {username} 创建异常: {e}")
            return False

    def _invite_cluster_members(cluster: str, members: list) -> bool:
        if not members:
            return True
        try:
            set_current_cluster(cluster)
            try:
                list_api = ListClusterMembersAPI(
                    enable_schema_validation=False,
                    response=None
                )
                list_api.query_params.page = "1"
                list_api.query_params.limit = "-1"
                list_api.query_params.sortBy = "createTime"
                res = list_api.send()
                if res.cached_response.raw_response.status_code == 200:
                    data = res.cached_response.raw_response.json()
                    existing_names = {x.get('metadata', {}).get('name') for x in data.get('items', [])}
                    to_invite = [m for m in members if m['username'] not in existing_names]
                    if not to_invite:
                        logger.info("集群成员已全部存在，跳过邀请")
                        return True
                else:
                    to_invite = members
            finally:
                clear_current_cluster()

            set_current_cluster(cluster)
            try:
                member_models = [V1beta1Member(username=mm['username'], roleRef=mm['roleRef']) for mm in to_invite]
                api = CreateClusterMembersAPI(
                    request_body=member_models,
                    enable_schema_validation=False,
                    response=None
                )
                res = api.send()
                if res.cached_response.raw_response.status_code in (200, 201):
                    invited = ", ".join([mm['username'] for mm in to_invite])
                    logger.info(f"集群成员 {invited} 邀请成功")
                else:
                    logger.warning(f"集群成员邀请失败: {res.cached_response.raw_response.status_code}")
            finally:
                clear_current_cluster()
        except Exception as e:
            if "already exists" in str(e).lower() or "409" in str(e):
                logger.info("集群成员已存在")
            else:
                logger.warning(f"集群成员邀请异常: {e}")
        return True

    def _invite_workspace_members(workspace: str, members: list) -> bool:
        if not members:
            return True
        try:
            list_api = ListWorkspaceMembersAPI(
                path_params=ListWorkspaceMembersAPI.PathParams(workspace=workspace),
                enable_schema_validation=False,
                response=None
            )
            list_api.query_params.page = "1"
            list_api.query_params.limit = "-1"
            list_api.query_params.sortBy = "createTime"
            res = list_api.send()
            if res.cached_response.raw_response.status_code == 200:
                data = res.cached_response.raw_response.json()
                existing_names = {x.get('metadata', {}).get('name') for x in data.get('items', [])}
                to_invite = [m for m in members if m['username'] not in existing_names]
                if not to_invite:
                    logger.info("企业空间成员已全部存在，跳过邀请")
                    return True
            else:
                to_invite = members

            member_models = [V1beta1Member(username=mm['username'], roleRef=mm['roleRef']) for mm in to_invite]
            api = CreateWorkspaceMembersAPI(
                path_params=CreateWorkspaceMembersAPI.PathParams(workspace=workspace),
                request_body=member_models,
                enable_schema_validation=False,
                response=None
            )
            res = api.send()
            if res.cached_response.raw_response.status_code in (200, 201):
                invited = ", ".join([mm['username'] for mm in to_invite])
                logger.info(f"企业空间成员 {invited} 邀请成功")
            else:
                logger.warning(f"企业空间成员邀请失败: {res.cached_response.raw_response.status_code}")
        except Exception as e:
            if "already exists" in str(e).lower() or "409" in str(e):
                logger.info("企业空间成员已存在")
            else:
                logger.warning(f"企业空间成员邀请异常: {e}")
        return True

    def _invite_namespace_members(cluster: str, namespace: str, members: list) -> bool:
        if not members:
            return True
        try:
            set_current_cluster(cluster)
            try:
                list_api = ListNamespaceMembersAPI(
                    path_params=ListNamespaceMembersAPI.PathParams(namespace=namespace),
                    enable_schema_validation=False,
                    response=None
                )
                list_api.query_params.page = "1"
                list_api.query_params.limit = "-1"
                list_api.query_params.sortBy = "createTime"
                res = list_api.send()
                if res.cached_response.raw_response.status_code == 200:
                    data = res.cached_response.raw_response.json()
                    existing_names = {x.get('metadata', {}).get('name') for x in data.get('items', [])}
                    to_invite = [m for m in members if m['username'] not in existing_names]
                    if not to_invite:
                        logger.info("项目成员已全部存在，跳过邀请")
                        return True
                else:
                    to_invite = members
            finally:
                clear_current_cluster()

            set_current_cluster(cluster)
            try:
                member_models = [V1beta1Member(username=mm['username'], roleRef=mm['roleRef']) for mm in to_invite]
                api = CreateNamespaceMembersAPI(
                    path_params=CreateNamespaceMembersAPI.PathParams(namespace=namespace),
                    request_body=member_models,
                    enable_schema_validation=False,
                    response=None
                )
                res = api.send()
                if res.cached_response.raw_response.status_code in (200, 201):
                    invited = ", ".join([mm['username'] for mm in to_invite])
                    logger.info(f"项目成员 {invited} 邀请成功")
                else:
                    logger.warning(f"项目成员邀请失败: {res.cached_response.raw_response.status_code}")
            finally:
                clear_current_cluster()
        except Exception as e:
            if "already exists" in str(e).lower() or "409" in str(e):
                logger.info("项目成员已存在")
            else:
                logger.warning(f"项目成员邀请异常: {e}")
        return True

    host_cluster, _ = get_clusters()
    if not host_cluster:
        logger.warning("无法获取 host 集群，跳过用户创建")
        return False

    logger.info("创建平台级用户...")
    for user in users_config.get('platform', []):
        _create_user(user['name'], user['email'], user['password'], user.get('globalRole'))

    logger.info("创建集群用户...")
    for user in users_config.get('cluster', []):
        _create_user(user['name'], user['email'], user['password'])

    logger.info("邀请集群用户加入 host 集群...")
    cluster_members = [{'username': u['name'], 'roleRef': u['clusterRole']} for u in users_config.get('cluster', [])]
    _invite_cluster_members(host_cluster, cluster_members)

    logger.info("创建企业空间用户...")
    for user in users_config.get('workspace', []):
        _create_user(user['name'], user['email'], user['password'])

    logger.info("邀请企业空间用户加入 ws-host-test...")
    ws_members = [{'username': u['name'], 'roleRef': u['workspaceRole']} for u in users_config.get('workspace', [])]
    _invite_workspace_members(workspace_name, ws_members)

    logger.info("创建项目用户...")
    for user in users_config.get('project', []):
        _create_user(user['name'], user['email'], user['password'])

    logger.info("邀请项目用户先加入企业空间 ws-host-test...")
    pro_ws_members = [{'username': u['name'], 'roleRef': u['workspaceRole']} for u in users_config.get('project', [])]
    _invite_workspace_members(workspace_name, pro_ws_members)

    logger.info("邀请项目用户加入项目 host-pro1-test...")
    pro_ns_members = [{'username': u['name'], 'roleRef': u['projectRole']} for u in users_config.get('project', [])]
    _invite_namespace_members(host_cluster, project_name, pro_ns_members)

    logger.info("测试用户创建完成")
    return True




