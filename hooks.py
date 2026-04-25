# -*- coding:utf-8 -*-
"""
全局钩子函数
- before_all: 所有测试开始前执行（数据初始化 + 并发预热告警规则组）

注意：aomaker 的 @hook 装饰器只在 pytest 之前执行，没有 after_all 区分
清理逻辑已移至 conftest.py 的 session_cleanup fixture
"""
import time
from loguru import logger
from aomaker.aomaker import hook
from utils.cluster_helpers import (
    setup_test_environment,
    get_clusters,
)
from testcases.test_api.whizard_alerting.base import prewarm_all_rule_groups


@hook
def before_all():
    """
    全局初始化 - 在所有测试开始前执行

    执行内容：
    1. 清理旧数据库
    2. 加载测试环境配置
    3. 创建测试企业空间和项目
    4. 并发预热所有标准告警规则组（global/cluster/namespace），等待告警触发
    """
    logger.info("=" * 60)
    logger.info("【全局初始化】开始准备测试数据...")
    logger.info("=" * 60)

    try:
        import os
        import glob
        db_files = glob.glob('database/*.db*')
        for f in db_files:
            if os.path.basename(f) == 'aomaker.db':
                continue
            try:
                os.remove(f)
            except Exception:
                pass

        host_cluster, member_cluster = get_clusters()
        if not host_cluster:
            logger.warning("无法获取Host集群信息，跳过数据初始化")
            return

        logger.info(f"集群信息获取成功")
        logger.info(f"  - Host集群: {host_cluster}")
        logger.info(f"  - Member集群: {member_cluster or '无'}")

        time.sleep(1.0)

        success, config = setup_test_environment()

        if success:
            logger.info("测试数据准备完成")
            workspaces = config.get('workspaces', {})
            projects = config.get('projects', {})

            host_ws = workspaces.get('host', {})
            host_proj = projects.get('host', {})
            logger.info(f"  - Host企业空间: {host_ws.get('name')}")
            logger.info(f"  - Host项目: {host_proj.get('name')}")

            test_namespace = host_proj.get('name', 'host-pro1-test')

            member_proj = None
            test_namespace_member = None
            if member_cluster:
                member_proj = projects.get('member', {})
                test_namespace_member = member_proj.get('name', 'mem-pro1-test')
                logger.info(f"  - Member企业空间: {workspaces.get('member', {}).get('name')}")
                logger.info(f"  - Member项目: {member_proj.get('name')}")

            logger.info("【并发预热】开始创建标准规则组并等待告警触发...")
            prewarm_all_rule_groups(
                host_cluster=host_cluster,
                test_namespace=test_namespace,
                member_cluster=member_cluster,
                test_namespace_member=test_namespace_member
            )
            logger.info("告警预热完成")
        else:
            logger.warning("测试数据准备失败，测试用例可能需要自行准备数据")

    except Exception as e:
        logger.warning(f"全局初始化发生异常: {e}")
        import traceback
        traceback.print_exc()
        logger.warning("测试用例可能需要自行准备数据")

    logger.info("=" * 60)
