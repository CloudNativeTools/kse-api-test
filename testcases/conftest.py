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


@pytest.fixture(scope="session", autouse=True)
def session_cleanup(request):
    """
    Session 级别 fixture
    在所有测试开始前如有 whizard_alerting 用例则预热规则组
    在所有测试结束后清理测试环境及预热规则组
    """
    from loguru import logger
    from utils.cluster_helpers import get_clusters
    from utils.test_data_helper import load_test_data

    has_alerting = any("whizard_alerting" in item.nodeid for item in request.session.items)

    if has_alerting:
        from testcases.test_api.whizard_alerting.base import prewarm_all_rule_groups

        host_cluster, member_cluster = get_clusters()
        if host_cluster:
            test_env = load_test_data("ks_core", "test_environment")
            test_namespace = test_env.get("projects", {}).get("host", {}).get("name", "host-pro1-test")
            test_namespace_member = None
            if member_cluster:
                test_namespace_member = test_env.get("projects", {}).get("member", {}).get("name", "mem-pro1-test")

            logger.info("【并发预热】开始创建标准规则组并等待告警触发...")
            prewarm_all_rule_groups(
                host_cluster=host_cluster,
                test_namespace=test_namespace,
                member_cluster=member_cluster,
                test_namespace_member=test_namespace_member,
            )
            logger.info("告警预热完成")

    yield

    from utils.cluster_helpers import get_clusters, cleanup_test_environment

    try:
        host_cluster, member_cluster = get_clusters()
        if host_cluster:
            if has_alerting:
                from testcases.test_api.whizard_alerting.base import cleanup_all_prewarmed_rule_groups
                test_env = load_test_data("ks_core", "test_environment")
                test_namespace = test_env.get("projects", {}).get("host", {}).get("name", "host-pro1-test")
                test_namespace_member = None
                if member_cluster:
                    test_namespace_member = test_env.get("projects", {}).get("member", {}).get("name", "mem-pro1-test")

                logger.info("开始清理预热规则组...")
                cleanup_all_prewarmed_rule_groups(
                    host_cluster=host_cluster,
                    test_namespace=test_namespace,
                    member_cluster=member_cluster,
                    test_namespace_member=test_namespace_member,
                )
                logger.info("预热规则组清理完成")
            cleanup_test_environment()
    except Exception as e:
        print(f"Session cleanup failed: {e}")
