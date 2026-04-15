# -*- coding:utf-8 -*-
"""
集群前缀中间件 - 默认给所有接口添加 /clusters/{cluster} 前缀
只排除不需要前缀的接口（集群管理类）
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
    for exclude in EXCLUDE_PATHS:
        if "{workspace}" in exclude:
            base = exclude.rsplit("/{workspace}", 1)[0]
            if path.startswith(base) and "/" not in path[len(base):]:
                return False
        elif path.startswith(exclude):
            return False
    return True


@middleware(name="cluster_prefix", priority=100, enabled=True)
def cluster_prefix_middleware(request: RequestType, call_next: CallNext):
    original_url = request.get("url", "")

    parsed = urlparse(original_url)
    path = parsed.path

    if not _should_add_cluster_prefix(path):
        return call_next(request)

    cluster_name = cache.get("current_cluster")
    if cluster_name:
        new_path = f"/clusters/{cluster_name}{path}"
        new_url = f"{parsed.scheme}://{parsed.netloc}{new_path}"
        if parsed.query:
            new_url += f"?{parsed.query}"
        request["url"] = new_url

    return call_next(request)
