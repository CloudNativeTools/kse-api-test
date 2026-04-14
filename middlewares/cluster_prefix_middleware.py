# -*- coding:utf-8 -*-
"""
集群前缀中间件 - 自动为资源类接口添加 /clusters/{cluster} 前缀
"""
from aomaker.core.middlewares.registry import middleware, RequestType, CallNext
from aomaker.storage import cache


# 需要添加 /clusters/xxx 前缀的接口路径模式
# 这些接口都是资源类接口（deployments、services、pods、namespaces等）
CLUSTER_PREFIX_PATHS = [
    "/kapis/resources.kubesphere.io",  # deployments、services等
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}/namespaces",  # 项目
    "/api/v1/namespaces",  # k8s原生命名空间
]

# 不需要添加前缀的接口（集群管理类）
EXCLUDE_PATHS = [
    "/kapis/tenant.kubesphere.io/v1alpha3/clusters",  # 集群列表
    "/kapis/tenant.kubesphere.io/v1beta1/clusters",  # 集群列表
    "/kapis/cluster.kubesphere.io",  # 集群管理
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces",  # 企业空间管理
    "/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates",  # 企业空间模板
]


def _should_add_cluster_prefix(path: str) -> bool:
    """
    判断是否需要添加 /clusters/xxx 前缀
    
    Args:
        path: 请求路径
        
    Returns:
        bool: 是否需要添加前缀
    """
    # 先检查是否在排除列表中
    for exclude in EXCLUDE_PATHS:
        if path.startswith(exclude):
            return False
    
    # 再检查是否需要添加前缀
    for prefix in CLUSTER_PREFIX_PATHS:
        if path.startswith(prefix):
            return True
    
    return False


@middleware(name="cluster_prefix", priority=100, enabled=True)
def cluster_prefix_middleware(request: RequestType, call_next: CallNext):
    """
    自动为资源类接口添加 /clusters/{cluster} 前缀
    
    工作流程：
    1. 检查请求路径是否需要添加集群前缀
    2. 从缓存或请求中获取当前集群名称
    3. 修改请求路径，添加 /clusters/{cluster} 前缀
    """
    original_path = request.get("url", "")
    
    # 检查是否需要添加前缀
    if not _should_add_cluster_prefix(original_path):
        return call_next(request)
    
    # 从缓存中获取集群名称
    cluster_name = cache.get("current_cluster")
    
    if cluster_name:
        # 添加 /clusters/{cluster} 前缀
        new_path = f"/clusters/{cluster_name}{original_path}"
        request["url"] = new_path
    
    return call_next(request)
