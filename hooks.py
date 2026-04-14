# -*- coding:utf-8 -*-
"""
全局钩子函数
- before_all: 所有测试开始前执行（数据初始化）
- after_all: 所有测试结束后执行（数据清理）

注意：这些钩子运行在主进程/线程中，在 pytest 之前/之后执行
"""
from aomaker.aomaker import hook
from utils.cluster_helpers import (
    setup_test_environment,
    cleanup_test_environment,
    get_clusters,
)


@hook
def before_all():
    """
    全局初始化 - 在所有测试开始前执行

    执行内容：
    1. 从 /data/api_data/_common/ 加载公共配置
    2. 从 /data/api_data/ks_core/test_environment.json 加载测试环境配置
    3. 获取集群信息（Host集群和Member集群）
    4. 创建测试企业空间和项目
       - Host集群：创建 ws-host-test 企业空间和 host-pro1-test 项目
       - Member集群（如有）：创建 ws-member-test 企业空间和 mem-pro1-test 项目

    如果初始化失败，会打印错误信息，但不会阻止测试执行
    （测试用例中可以通过 get_for_test() 再次尝试准备数据）
    """
    print("=" * 60)
    print("【全局初始化】开始准备测试数据...")
    print("=" * 60)

    try:
        # 1. 获取集群信息
        host_cluster, member_cluster = get_clusters()
        if not host_cluster:
            print("⚠️ 警告: 无法获取Host集群信息，跳过数据初始化")
            return

        print(f"✓ 集群信息获取成功")
        print(f"  - Host集群: {host_cluster}")
        print(f"  - Member集群: {member_cluster or '无'}")

        # 2. 创建测试环境（从配置文件加载数据）
        success, config = setup_test_environment()

        if success:
            print("✓ 测试数据准备完成")
            workspaces = config.get('workspaces', {})
            projects = config.get('projects', {})
            
            host_ws = workspaces.get('host', {})
            host_proj = projects.get('host', {})
            print(f"  - Host集群: {host_ws.get('name')} / {host_proj.get('name')}")
            
            if member_cluster:
                member_ws = workspaces.get('member', {})
                member_proj = projects.get('member', {})
                print(f"  - Member集群: {member_ws.get('name')} / {member_proj.get('name')}")
        else:
            print("⚠️ 警告: 测试数据准备失败，测试用例可能需要自行准备数据")

    except Exception as e:
        print(f"⚠️ 警告: 全局初始化发生异常: {e}")
        print("  测试用例可能需要自行准备数据")

    print("=" * 60)
    print()


@hook
def after_all():
    """
    全局清理 - 在所有测试结束后执行

    执行内容：
    1. 从 /data/api_data/ks_core/test_environment.json 加载测试环境配置
    2. 删除测试创建的企业空间和项目
       - Host集群：删除 ws-host-test 企业空间和 host-pro1-test 项目
       - Member集群（如有）：删除 ws-member-test 企业空间和 mem-pro1-test 项目

    注意：清理操作会忽略资源不存在的错误，确保清理过程不会失败
    """
    print()
    print("=" * 60)
    print("【全局清理】开始清理测试数据...")
    print("=" * 60)

    try:
        # 清理测试数据（从配置文件加载数据）
        success, config = cleanup_test_environment()

        if success:
            print("✓ 测试数据清理完成")
            workspaces = config.get('workspaces', {})
            projects = config.get('projects', {})
            
            host_ws = workspaces.get('host', {})
            host_proj = projects.get('host', {})
            print(f"  - Host集群: {host_ws.get('name')} / {host_proj.get('name')}")
            
            _, member_cluster = get_clusters()
            if member_cluster:
                member_ws = workspaces.get('member', {})
                member_proj = projects.get('member', {})
                print(f"  - Member集群: {member_ws.get('name')} / {member_proj.get('name')}")
        else:
            print("⚠️ 警告: 测试数据清理可能未完全完成")

    except Exception as e:
        print(f"⚠️ 警告: 全局清理发生异常: {e}")
        print("  部分测试数据可能未完全清理")

    print("=" * 60)
