# -*- coding:utf-8 -*-
"""
全局测试配置 - 公共 fixtures
供所有测试用例复用
"""
import logging
import pytest
from utils.cluster_helpers import get_clusters
from utils.test_data_helper import load_test_data


def pytest_configure(config):
    """配置 logging，让 logger 输出到控制台"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


@pytest.fixture(scope="session")
def host_cluster():
    """
    获取 host 集群
    所有环境必须有 host 集群
    """
    host, _ = get_clusters()
    if not host:
        pytest.skip("无 host 集群")
    return host


@pytest.fixture(scope="session")
def member_cluster():
    """
    获取 member 集群
    单集群环境自动跳过标记了 @pytest.mark.multi_cluster 的测试
    """
    _, member = get_clusters()
    if not member:
        pytest.skip("无 member 集群，单集群环境跳过")
    return member


@pytest.fixture(scope="session")
def clusters():
    """
    获取所有集群信息
    返回 (host_cluster_name, member_cluster_name)
    member_cluster 可能为 None（单集群环境）
    """
    return get_clusters()


@pytest.fixture(scope="session")
def test_namespace():
    """
    获取 Host 集群测试命名空间
    使用 hooks.py 创建的测试项目 host-pro1-test
    """
    test_env = load_test_data("ks_core", "test_environment")
    return test_env.get("projects", {}).get("host", {}).get("name", "host-pro1-test")


@pytest.fixture(scope="session")
def test_namespace_member():
    """
    获取 Member 集群测试命名空间
    使用 hooks.py 创建的测试项目 mem-pro1-test
    单集群环境返回 None
    """
    host, member = get_clusters()
    if not member:
        return None
    
    test_env = load_test_data("ks_core", "test_environment")
    return test_env.get("projects", {}).get("member", {}).get("name", "mem-pro1-test")
