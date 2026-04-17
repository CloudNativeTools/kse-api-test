# -*- coding:utf-8 -*-
import pytest
import time

from apis.whizard_alerting.Alerting_Management.apis import (
    HandleListClusterAlertsAPI,
    HandleListClusterRuleGroupsAPI,
    HandleCreateClusterRuleGroupAPI,
    HandleGetClusterRuleGroupAPI,
    HandleUpdateClusterRuleGroupAPI,
    HandleDeleteClusterRuleGroupAPI,
    HandlePatchClusterRuleGroupAPI,
    HandleListAlertsAPI,
    HandleListRuleGroupsAPI,
    HandleCreateRuleGroupAPI,
    HandleGetRuleGroupAPI,
    HandleUpdateRuleGroupAPI,
    HandleDeleteRuleGroupAPI,
    HandlePatchRuleGroupAPI,
    HandleListGlobalAlertsAPI,
    HandleListGlobalRuleGroupsAPI,
    HandleCreateGlobalRuleGroupAPI,
    HandleGetGlobalRuleGroupAPI,
    HandleUpdateGlobalRuleGroupAPI,
    HandleDeleteGlobalRuleGroupAPI,
    HandlePatchGlobalRuleGroupAPI,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import get_clusters, set_current_cluster, clear_current_cluster


# 测试数据路径
TEST_DATA_PATH = "whizard_alerting/Alerting_Management"


# ==================== get_for_test 函数 ====================

def get_for_test_global_rule_group(group_name: str) -> bool:
    """
    获取全局规则组测试数据
    1. 先查询，如果测试数据已存在，直接返回 True
    2. 如果测试数据不存在，调用创建 API 创建测试数据
    3. 创建成功返回 True，失败返回 False
    """
    try:
        # 1. 查询现有数据
        list_api = HandleListGlobalRuleGroupsAPI(enable_schema_validation=False)
        res = list_api.send()
        
        if res.cached_response.raw_response.status_code != 200:
            return False
        
        data = res.cached_response.raw_response.json()
        
        # 2. 检查测试数据是否已存在
        for item in data.get("items", []):
            if item.get("metadata", {}).get("name") == group_name:
                return True
        
        # 3. 测试数据不存在，创建它
        request_body = load_test_data(TEST_DATA_PATH, "global_rule_groups", "test_global_rule_group")
        request_body["metadata"]["name"] = group_name
        
        create_api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        create_res = create_api.send()
        
        if create_res.cached_response.raw_response.status_code in (200, 201):
            return True
        return False
        
    except Exception:
        return False


def get_for_test_cluster_rule_group(cluster: str, group_name: str) -> bool:
    """
    获取集群规则组测试数据
    """
    try:
        # 设置当前集群，让中间件自动添加 /clusters/{cluster} 前缀
        set_current_cluster(cluster)
        
        try:
            # 1. 查询现有数据
            list_api = HandleListClusterRuleGroupsAPI(enable_schema_validation=False)
            list_api.path_params = HandleListClusterRuleGroupsAPI.PathParams(cluster=cluster)
            res = list_api.send()
            
            if res.cached_response.raw_response.status_code != 200:
                return False
            
            data = res.cached_response.raw_response.json()
            
            # 2. 检查测试数据是否已存在
            for item in data.get("items", []):
                if item.get("metadata", {}).get("name") == group_name:
                    return True
            
            # 3. 测试数据不存在，创建它
            request_body = load_test_data(TEST_DATA_PATH, "cluster_rule_groups", "test_cluster_rule_group")
            request_body["metadata"]["name"] = group_name
            
            create_api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            create_res = create_api.send()
            
            if create_res.cached_response.raw_response.status_code in (200, 201):
                return True
            return False
        finally:
            clear_current_cluster()
        
    except Exception:
        return False


def get_for_test_namespace_rule_group(cluster: str, namespace: str, group_name: str) -> bool:
    """
    获取命名空间规则组测试数据
    """
    try:
        # 设置当前集群，让中间件自动添加 /clusters/{cluster} 前缀
        set_current_cluster(cluster)
        
        try:
            # 1. 查询现有数据
            list_api = HandleListRuleGroupsAPI(enable_schema_validation=False)
            list_api.path_params = HandleListRuleGroupsAPI.PathParams(cluster=cluster, namespace=namespace)
            res = list_api.send()
            
            if res.cached_response.raw_response.status_code != 200:
                return False
            
            data = res.cached_response.raw_response.json()
            
            # 2. 检查测试数据是否已存在
            for item in data.get("items", []):
                if item.get("metadata", {}).get("name") == group_name:
                    return True
            
            # 3. 测试数据不存在，创建它
            request_body = load_test_data(TEST_DATA_PATH, "namespace_rule_groups", "test_namespace_rule_group")
            request_body["metadata"]["name"] = group_name
            
            create_api = HandleCreateRuleGroupAPI(
                path_params=HandleCreateRuleGroupAPI.PathParams(cluster=cluster, namespace=namespace),
                request_body=request_body,
                enable_schema_validation=False
            )
            create_res = create_api.send()
            
            if create_res.cached_response.raw_response.status_code in (200, 201):
                return True
            return False
        finally:
            clear_current_cluster()
        
    except Exception:
        return False


# ==================== 列表查询类接口 ====================

@pytest.mark.alerting_management
def test_list_cluster_alerts_success():
    """获取集群告警列表"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    set_current_cluster(host_cluster)
    try:
        api = HandleListClusterAlertsAPI(
            path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster),
            enable_schema_validation=False
        )
        api.query_params.page = "1"
        api.query_params.ascending = "false"
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data
    finally:
        clear_current_cluster()


@pytest.mark.alerting_management
def test_list_cluster_rule_groups_success():
    """获取集群告警规则组列表"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    set_current_cluster(host_cluster)
    try:
        api = HandleListClusterRuleGroupsAPI(enable_schema_validation=False)
        api.path_params = HandleListClusterRuleGroupsAPI.PathParams(cluster=host_cluster)
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data
    finally:
        clear_current_cluster()


@pytest.mark.alerting_management
def test_list_global_alerts_success():
    """获取全局告警列表"""
    api = HandleListGlobalAlertsAPI(enable_schema_validation=False)
    api.query_params.page = "1"
    api.query_params.ascending = "false"
    res = api.send()
    assert res.cached_response.raw_response.status_code == 200

    data = res.cached_response.raw_response.json()
    assert "items" in data
    assert "totalItems" in data


@pytest.mark.alerting_management
def test_list_global_rule_groups_success():
    """获取全局告警规则组列表"""
    api = HandleListGlobalRuleGroupsAPI(enable_schema_validation=False)
    api.query_params.page = "1"
    api.query_params.ascending = "false"
    res = api.send()
    assert res.cached_response.raw_response.status_code == 200

    data = res.cached_response.raw_response.json()
    assert "items" in data
    assert "totalItems" in data


@pytest.mark.alerting_management
def test_list_namespace_alerts_success():
    """获取命名空间告警列表"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    set_current_cluster(host_cluster)
    try:
        api = HandleListAlertsAPI(enable_schema_validation=False)
        api.path_params = HandleListAlertsAPI.PathParams(
            cluster=host_cluster,
            namespace="host-pro1-test"
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data
    finally:
        clear_current_cluster()


@pytest.mark.alerting_management
def test_list_namespace_rule_groups_success():
    """获取命名空间告警规则组列表"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    set_current_cluster(host_cluster)
    try:
        api = HandleListRuleGroupsAPI(enable_schema_validation=False)
        api.path_params = HandleListRuleGroupsAPI.PathParams(
            cluster=host_cluster,
            namespace="host-pro1-test"
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data
    finally:
        clear_current_cluster()


# ==================== 创建类接口 ====================

@pytest.mark.alerting_management
def test_create_global_rule_group_success():
    """创建全局告警规则组"""
    group_name = f"test-global-rule-group-{int(time.time())}"
    
    request_body = {
        "apiVersion": "alerting.kubesphere.io/v2beta1",
        "kind": "GlobalRuleGroup",
        "metadata": {
            "name": group_name
        },
        "spec": {
            "rules": [
                {
                    "alert": "TestGlobalAlert",
                    "expr": "up == 1",
                    "for": "1m",
                    "labels": {
                        "severity": "warning"
                    },
                    "annotations": {
                        "summary": "Test global alert summary",
                        "message": "Test global alert message"
                    }
                }
            ]
        }
    }
    
    create_api = HandleCreateGlobalRuleGroupAPI(
        request_body=request_body,
        enable_schema_validation=False
    )
    create_res = create_api.send()
    assert create_res.cached_response.raw_response.status_code == 201

    # 验证创建成功
    get_api = HandleGetGlobalRuleGroupAPI()
    get_api.path_params = HandleGetGlobalRuleGroupAPI.PathParams(name=group_name)
    get_res = get_api.send()
    assert get_res.cached_response.raw_response.status_code == 200

    data = get_res.cached_response.raw_response.json()
    assert data.get("metadata", {}).get("name") == group_name


@pytest.mark.alerting_management
def test_create_cluster_rule_group_success():
    """创建集群告警规则组"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    group_name = f"test-cluster-rule-group-{int(time.time())}"
    
    set_current_cluster(host_cluster)
    try:
        request_body = {
            "apiVersion": "alerting.kubesphere.io/v2beta1",
            "kind": "ClusterRuleGroup",
            "metadata": {
                "name": group_name
            },
            "spec": {
                "rules": [
                    {
                        "alert": "TestClusterAlert",
                        "expr": "up == 1",
                        "for": "1m",
                        "labels": {
                            "severity": "warning"
                        },
                        "annotations": {
                            "summary": "Test cluster alert summary"
                        }
                    }
                ]
            }
        }
        
        create_api = HandleCreateClusterRuleGroupAPI(
            path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=host_cluster),
            request_body=request_body,
            enable_schema_validation=False
        )
        create_res = create_api.send()
        assert create_res.cached_response.raw_response.status_code == 201

        # 验证创建成功
        get_api = HandleGetClusterRuleGroupAPI()
        get_api.path_params = HandleGetClusterRuleGroupAPI.PathParams(
            cluster=host_cluster,
            name=group_name
        )
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code == 200

        data = get_res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == group_name
    finally:
        clear_current_cluster()


@pytest.mark.alerting_management
def test_create_namespace_rule_group_success():
    """创建命名空间告警规则组"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    group_name = f"test-ns-rule-group-{int(time.time())}"
    namespace = "host-pro1-test"
    
    set_current_cluster(host_cluster)
    try:
        request_body = {
            "apiVersion": "alerting.kubesphere.io/v2beta1",
            "kind": "RuleGroup",
            "metadata": {
                "name": group_name
            },
            "spec": {
                "rules": [
                    {
                        "alert": "TestNamespaceAlert",
                        "expr": "up == 1",
                        "for": "1m",
                        "labels": {
                            "severity": "warning"
                        },
                        "annotations": {
                            "summary": "Test namespace alert summary"
                        }
                    }
                ]
            }
        }
        
        create_api = HandleCreateRuleGroupAPI(
            path_params=HandleCreateRuleGroupAPI.PathParams(
                cluster=host_cluster,
                namespace=namespace
            ),
            request_body=request_body
        )
        create_res = create_api.send()
        assert create_res.cached_response.raw_response.status_code == 201

        # 验证创建成功
        get_api = HandleGetRuleGroupAPI()
        get_api.path_params = HandleGetRuleGroupAPI.PathParams(
            cluster=host_cluster,
            namespace=namespace,
            name=group_name
        )
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code == 200

        data = get_res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == group_name
    finally:
        clear_current_cluster()


# ==================== 删除类接口 ====================

@pytest.mark.alerting_management
def test_delete_global_rule_group_success():
    """删除全局告警规则组 - 使用 get_for_test 准备数据"""
    group_name = f"test-delete-global-{int(time.time())}"
    
    # 准备测试数据（创建规则组）
    if not get_for_test_global_rule_group(group_name):
        pytest.skip("无法准备测试数据")
    
    # 删除规则组
    delete_api = HandleDeleteGlobalRuleGroupAPI()
    delete_api.path_params = HandleDeleteGlobalRuleGroupAPI.PathParams(name=group_name)
    delete_res = delete_api.send()
    assert delete_res.cached_response.raw_response.status_code == 200
    
    # 验证已删除
    get_api = HandleGetGlobalRuleGroupAPI()
    get_api.path_params = HandleGetGlobalRuleGroupAPI.PathParams(name=group_name)
    get_api.enable_schema_validation = False
    get_res = get_api.send()
    assert get_res.cached_response.raw_response.status_code in [404, 500]


@pytest.mark.alerting_management
def test_delete_cluster_rule_group_success():
    """删除集群告警规则组 - 使用 get_for_test 准备数据"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    group_name = f"test-delete-cluster-{int(time.time())}"
    
    # 准备测试数据（创建规则组）
    if not get_for_test_cluster_rule_group(host_cluster, group_name):
        pytest.skip("无法准备测试数据")
    
    set_current_cluster(host_cluster)
    try:
        # 删除规则组
        delete_api = HandleDeleteClusterRuleGroupAPI()
        delete_api.path_params = HandleDeleteClusterRuleGroupAPI.PathParams(
            cluster=host_cluster,
            name=group_name
        )
        delete_res = delete_api.send()
        assert delete_res.cached_response.raw_response.status_code == 200
        
        # 验证已删除
        get_api = HandleGetClusterRuleGroupAPI()
        get_api.path_params = HandleGetClusterRuleGroupAPI.PathParams(
            cluster=host_cluster,
            name=group_name
        )
        get_api.enable_schema_validation = False
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code in [404, 500]
    finally:
        clear_current_cluster()


@pytest.mark.alerting_management
def test_delete_namespace_rule_group_success():
    """删除命名空间告警规则组 - 使用 get_for_test 准备数据"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    group_name = f"test-delete-ns-{int(time.time())}"
    namespace = "host-pro1-test"
    
    # 准备测试数据（创建规则组）
    if not get_for_test_namespace_rule_group(host_cluster, namespace, group_name):
        pytest.skip("无法准备测试数据")
    
    set_current_cluster(host_cluster)
    try:
        # 删除规则组
        delete_api = HandleDeleteRuleGroupAPI()
        delete_api.path_params = HandleDeleteRuleGroupAPI.PathParams(
            cluster=host_cluster,
            namespace=namespace,
            name=group_name
        )
        delete_res = delete_api.send()
        assert delete_res.cached_response.raw_response.status_code == 200
        
        # 验证已删除
        get_api = HandleGetRuleGroupAPI()
        get_api.path_params = HandleGetRuleGroupAPI.PathParams(
            cluster=host_cluster,
            namespace=namespace,
            name=group_name
        )
        get_api.enable_schema_validation = False
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code in [404, 500]
    finally:
        clear_current_cluster()


# ==================== 更新类接口 ====================

@pytest.mark.alerting_management
def test_update_global_rule_group_success():
    """更新全局告警规则组 - 使用 get_for_test 准备数据"""
    group_name = f"test-update-global-{int(time.time())}"
    
    # 准备测试数据
    if not get_for_test_global_rule_group(group_name):
        pytest.skip("无法准备测试数据")
    
    # 加载更新数据
    update_body = load_test_data(TEST_DATA_PATH, "global_rule_groups", "updated_global_rule_group")
    update_body["metadata"]["name"] = group_name
    
    update_api = HandleUpdateGlobalRuleGroupAPI(
        path_params=HandleUpdateGlobalRuleGroupAPI.PathParams(name=group_name),
        request_body=update_body,
        enable_schema_validation=False
    )
    res = update_api.send()
    assert res.cached_response.raw_response.status_code == 200

    # 验证更新成功
    get_api = HandleGetGlobalRuleGroupAPI()
    get_api.path_params = HandleGetGlobalRuleGroupAPI.PathParams(name=group_name)
    get_res = get_api.send()
    data = get_res.cached_response.raw_response.json()
    
    rules = data.get("spec", {}).get("rules", [])
    assert len(rules) > 0
    assert rules[0].get("alert") == "TestGlobalAlertUpdated"
    
    # 清理
    delete_api = HandleDeleteGlobalRuleGroupAPI()
    delete_api.path_params = HandleDeleteGlobalRuleGroupAPI.PathParams(name=group_name)
    delete_api.send()


@pytest.mark.alerting_management
def test_update_cluster_rule_group_success():
    """更新集群告警规则组 - 使用 get_for_test 准备数据"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    group_name = f"test-update-cluster-{int(time.time())}"
    
    # 准备测试数据
    if not get_for_test_cluster_rule_group(host_cluster, group_name):
        pytest.skip("无法准备测试数据")
    
    set_current_cluster(host_cluster)
    try:
        # 更新规则组
        update_body = {
            "apiVersion": "alerting.kubesphere.io/v2beta1",
            "kind": "ClusterRuleGroup",
            "metadata": {
                "name": group_name
            },
            "spec": {
                "rules": [
                    {
                        "alert": "TestClusterAlertUpdated",
                        "expr": "up == 0",
                        "for": "5m",
                        "labels": {
                            "severity": "critical"
                        },
                        "annotations": {
                            "summary": "Updated cluster alert summary"
                        }
                    }
                ]
            }
        }
        
        update_api = HandleUpdateClusterRuleGroupAPI(
            path_params=HandleUpdateClusterRuleGroupAPI.PathParams(
                cluster=host_cluster,
                name=group_name
            ),
            request_body=update_body,
            enable_schema_validation=False
        )
        res = update_api.send()
        assert res.cached_response.raw_response.status_code == 200

        # 验证更新成功
        get_api = HandleGetClusterRuleGroupAPI()
        get_api.path_params = HandleGetClusterRuleGroupAPI.PathParams(
            cluster=host_cluster,
            name=group_name
        )
        get_res = get_api.send()
        data = get_res.cached_response.raw_response.json()
        
        rules = data.get("spec", {}).get("rules", [])
        assert len(rules) > 0
        assert rules[0].get("alert") == "TestClusterAlertUpdated"
    finally:
        clear_current_cluster()
    
    # 清理
    set_current_cluster(host_cluster)
    try:
        delete_api = HandleDeleteClusterRuleGroupAPI()
        delete_api.path_params = HandleDeleteClusterRuleGroupAPI.PathParams(
            cluster=host_cluster,
            name=group_name
        )
        delete_api.send()
    finally:
        clear_current_cluster()


@pytest.mark.alerting_management
def test_update_namespace_rule_group_success():
    """更新命名空间告警规则组 - 使用 get_for_test 准备数据"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    group_name = f"test-update-ns-{int(time.time())}"
    namespace = "host-pro1-test"
    
    # 准备测试数据
    if not get_for_test_namespace_rule_group(host_cluster, namespace, group_name):
        pytest.skip("无法准备测试数据")
    
    set_current_cluster(host_cluster)
    try:
        # 加载更新数据
        update_body = load_test_data(TEST_DATA_PATH, "namespace_rule_groups", "updated_namespace_rule_group")
        update_body["metadata"]["name"] = group_name
        
        update_api = HandleUpdateRuleGroupAPI(
            path_params=HandleUpdateRuleGroupAPI.PathParams(
                cluster=host_cluster,
                namespace=namespace,
                name=group_name
            ),
            request_body=update_body,
            enable_schema_validation=False
        )
        res = update_api.send()
        assert res.cached_response.raw_response.status_code == 200

        # 验证更新成功
        get_api = HandleGetRuleGroupAPI()
        get_api.path_params = HandleGetRuleGroupAPI.PathParams(
            cluster=host_cluster,
            namespace=namespace,
            name=group_name
        )
        get_res = get_api.send()
        data = get_res.cached_response.raw_response.json()
        
        rules = data.get("spec", {}).get("rules", [])
        assert len(rules) > 0
        assert rules[0].get("alert") == "TestNamespaceAlertUpdated"
    finally:
        clear_current_cluster()
    
    # 清理
    set_current_cluster(host_cluster)
    try:
        delete_api = HandleDeleteRuleGroupAPI()
        delete_api.path_params = HandleDeleteRuleGroupAPI.PathParams(
            cluster=host_cluster,
            namespace=namespace,
            name=group_name
        )
        delete_api.send()
    finally:
        clear_current_cluster()


# ==================== Patch 类接口 ====================

@pytest.mark.alerting_management
def test_patch_global_rule_group_success():
    """Patch 更新全局告警规则组状态 - 使用 get_for_test 准备数据"""
    group_name = f"test-patch-global-{int(time.time())}"
    
    # 准备测试数据
    if not get_for_test_global_rule_group(group_name):
        pytest.skip("无法准备测试数据")
    
    # 加载 patch 数据
    patch_body = load_test_data(TEST_DATA_PATH, "global_rule_groups", "patched_global_rule_group")
    patch_body["metadata"]["name"] = group_name
    
    patch_api = HandlePatchGlobalRuleGroupAPI(
        path_params=HandlePatchGlobalRuleGroupAPI.PathParams(name=group_name),
        request_body=patch_body,
        enable_schema_validation=False
    )
    res = patch_api.send()
    # Patch 可能返回 200 或 202
    assert res.cached_response.raw_response.status_code in [200, 202]
    
    # 清理
    delete_api = HandleDeleteGlobalRuleGroupAPI()
    delete_api.path_params = HandleDeleteGlobalRuleGroupAPI.PathParams(name=group_name)
    delete_api.send()


# ==================== 错误处理类接口 ====================

@pytest.mark.alerting_management
def test_get_nonexistent_global_rule_group():
    """获取不存在的全局规则组 - 验证错误处理"""
    api = HandleGetGlobalRuleGroupAPI(
        path_params=HandleGetGlobalRuleGroupAPI.PathParams(name="nonexistent-rule-group-12345"),
        enable_schema_validation=False
    )
    res = api.send()
    
    assert res.cached_response.raw_response.status_code in [404, 500]


@pytest.mark.alerting_management
def test_delete_nonexistent_global_rule_group():
    """删除不存在的全局规则组 - 验证错误处理"""
    api = HandleDeleteGlobalRuleGroupAPI(
        path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(name="nonexistent-rule-group-12345"),
        enable_schema_validation=False
    )
    res = api.send()
    
    # 删除不存在资源可能返回 200 或 404
    assert res.cached_response.raw_response.status_code in [200, 404]
