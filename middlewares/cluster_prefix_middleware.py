# -*- coding:utf-8 -*-
"""
集群前缀中间件 - 自动为资源类接口添加 /clusters/{cluster} 前缀
支持多种路径格式：
- ks-core 格式: /clusters/{cluster}/kapis/xxx
- whizard-alerting 格式: /proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/xxx
"""
from urllib.parse import urlparse
from aomaker.core.middlewares.registry import middleware, RequestType, CallNext
from aomaker.storage import cache

EXCLUDE_PATHS = [
    "/kapis/tenant.kubesphere.io/v1alpha3/clusters",
    "/kapis/tenant.kubesphere.io/v1beta1/clusters",
    "/kapis/cluster.kubesphere.io",
    "/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates",
    "/kapis/tenant.kubesphere.io/v1beta1/workspaces/{workspace}",
]


def _should_add_cluster_prefix(path: str) -> bool:
    """判断是否需要添加集群前缀"""
    for exclude in EXCLUDE_PATHS:
        if "{workspace}" in exclude:
            base = exclude.rsplit("/{workspace}", 1)[0]
            if path.startswith(base) and "/" not in path[len(base):]:
                return False
        elif path.startswith(exclude):
            return False
    return True


def _add_cluster_prefix_to_alerting(path: str, cluster: str) -> str:
    """
    为 whizard-alerting 路径添加 /proxy 前缀
    
    全局API (包含 'global' 的路径):
      swagger: /alerting.kubesphere.io/v2beta1/globalrulegroups
      实际:    /proxy/alerting.kubesphere.io/v2beta1/globalrulegroups
    
    集群/命名空间API (包含 'clusters/{cluster}' 的路径):
      swagger: /alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusteralerts
      实际:    /proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/clusteralerts
    
    所以只需要在开头添加 /proxy，路径中已有的 clusters/{cluster} 或 global 保持不变
    """
    # 如果已经有 proxy 前缀，不再添加
    if path.startswith("/proxy/"):
        return path
    
    # 在开头添加 /proxy
    return f"/proxy{path}"


def _add_cluster_prefix_to_kapis(path: str, cluster: str) -> str:
    """
    为 ks-core 路径添加集群前缀（标准格式）
    
    原始路径: /kapis/resources.kubesphere.io/v1alpha3/deployments
    处理后:   /clusters/{cluster}/kapis/resources.kubesphere.io/v1alpha3/deployments
    """
    return f"/clusters/{cluster}{path}"


@middleware(name="cluster_prefix", priority=100, enabled=True)
def cluster_prefix_middleware(request: RequestType, call_next: CallNext):
    """
    自动为资源类接口添加 /clusters/{cluster} 前缀
    
    支持两种路径格式：
    1. ks-core: /clusters/{cluster}/kapis/xxx
    2. whizard-alerting: /proxy/alerting.kubesphere.io/v2beta1/xxx
    """
    original_url = request.get("url", "")

    parsed = urlparse(original_url)
    path = parsed.path

    if not _should_add_cluster_prefix(path):
        return call_next(request)

    cluster_name = cache.get("current_cluster")
    
    # 根据路径类型选择不同的处理方式
    if path.startswith("/alerting.kubesphere.io"):
        # whizard-alerting 格式 - 总是添加 /proxy 前缀
        # 全局API: /proxy/alerting.kubesphere.io/v2beta1/globalrulegroups
        # 集群API: /proxy/alerting.kubesphere.io/v2beta1/clusters/{cluster}/xxx
        new_path = _add_cluster_prefix_to_alerting(path, cluster_name or "")
    else:
        # ks-core 标准格式 - 需要 cluster_name
        if not cluster_name:
            return call_next(request)
        new_path = _add_cluster_prefix_to_kapis(path, cluster_name)
    
    new_url = f"{parsed.scheme}://{parsed.netloc}{new_path}"
    if parsed.query:
        new_url += f"?{parsed.query}"
    request["url"] = new_url

    return call_next(request)
