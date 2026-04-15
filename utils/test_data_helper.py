# -*- coding:utf-8 -*-
"""
测试数据加载公共工具
支持运行时变量替换
"""
import json
import re
import time
import random
import string
from pathlib import Path
from typing import Any, List, Dict, Union

from aomaker.storage import cache


def generate_random_string(length: int = 8) -> str:
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def get_variable_value(var_name: str) -> str:
    """
    获取变量值
    
    支持的变量：
    - {{random}}: 随机字符串
    - {{timestamp}}: 当前时间戳
    - {{date}}: 当前日期
    - {{host_cluster}}: Host 集群名称
    - {{member_cluster}}: Member 集群名称
    - {{admin_user}}: 管理员用户名
    - {{admin_password}}: 管理员密码
    - {{test_user}}: 测试用户名
    - {{workspaces.host.name}}: Host 企业空间名称
    - {{workspaces.member.name}}: Member 企业空间名称
    - {{projects.host.name}}: Host 项目名称
    - {{projects.member.name}}: Member 项目名称
    """
    try:
        var_mapping = {
            'random': generate_random_string(8),
            'timestamp': str(int(time.time())),
            'date': time.strftime('%Y%m%d'),
        }
        
        # 尝试从 cache 获取集群信息（如果失败，使用默认值）
        try:
            var_mapping['host_cluster'] = cache.get('host_cluster') or 'host'
            var_mapping['member_cluster'] = cache.get('member_cluster') or ''
        except Exception as e:
            print(f"⚠️ 警告: 获取集群缓存失败，使用默认值: {e}")
            var_mapping['host_cluster'] = 'host'
            var_mapping['member_cluster'] = ''
        
        # 尝试从配置文件获取用户信息
        try:
            var_mapping['admin_user'] = _get_nested_value('test_users', 'admin', 'username')
            var_mapping['admin_password'] = _get_nested_value('test_users', 'admin', 'password')
            var_mapping['test_user'] = _get_nested_value('test_users', 'test_user', 'username')
        except Exception as e:
            print(f"⚠️ 警告: 获取用户配置失败: {e}")
            var_mapping['admin_user'] = 'admin'
            var_mapping['admin_password'] = 'admin'
            var_mapping['test_user'] = 'test_user'
        
        # 处理嵌套变量，如 workspaces.host.name
        if '.' in var_name:
            parts = var_name.split('.')
            if len(parts) == 3 and parts[0] in ['workspaces', 'projects']:
                try:
                    return _get_workspace_or_project_name(parts[0], parts[1], parts[2])
                except Exception as e:
                    print(f"⚠️ 警告: 获取 {var_name} 失败: {e}")
                    return f'{{{{{var_name}}}}}'
        
        return var_mapping.get(var_name, f'{{{{unknown:{var_name}}}}}')
    except Exception as e:
        # 如果获取变量失败，返回原始占位符
        print(f"⚠️ 警告: 获取变量 {var_name} 失败: {e}")
        return f'{{{{{var_name}}}}}'


def _get_nested_value(component: str, key: str, field: str) -> str:
    """
    获取嵌套值（直接从配置文件读取，不依赖 cache）
    
    Args:
        component: 组件名称，如 "test_users"
        key: 顶层键名，如 "admin"
        field: 字段名，如 "username"
    
    Returns:
        str: 字段值，如果获取失败返回默认值
    """
    try:
        # 直接读取配置文件，不进行变量替换，避免连锁错误
        data_key = f"{key}.{field}"
        config = load_test_data('_common', component, data_key=data_key, default={}, replace_vars=False)
        return config if config else key
    except Exception as e:
        print(f"⚠️ 警告: 获取嵌套值 {component}.{key}.{field} 失败: {e}")
        return key


def _get_workspace_or_project_name(data_type: str, cluster_type: str, field: str) -> str:
    """获取企业空间或项目名称"""
    config = load_test_data('ks_core', 'test_environment', data_type, {})
    cluster_config = config.get(cluster_type, {})
    return cluster_config.get(field, '')


def replace_variables(data: Any) -> Any:
    """
    递归替换数据中的变量
    
    Args:
        data: 原始数据（可以是 dict、list、str 等）
    
    Returns:
        替换变量后的数据
    """
    if isinstance(data, dict):
        return {key: replace_variables(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_variables(item) for item in data]
    elif isinstance(data, str):
        # 匹配 {{variable}} 格式
        pattern = r'\{\{(\w+(?:\.\w+)*)\}\}'
        
        def replace_match(match):
            var_name = match.group(1)
            return get_variable_value(var_name)
        
        return re.sub(pattern, replace_match, data)
    else:
        return data


def load_test_data(
    component: str, 
    module: str, 
    data_key: str = None, 
    default: Any = None,
    replace_vars: bool = True
) -> Any:
    """
    从JSON文件加载测试数据
    
    Args:
        component: 组件名称，如 "ks_core"、"_common"
        module: 模块名称，如 "access_management"、"test_users"
        data_key: 数据键名，如 "test_roles"，为None时返回整个文件内容
        default: 默认值
        replace_vars: 是否替换变量，默认为True
    
    Returns:
        测试数据（已替换变量）
    
    Examples:
        # 加载公共用户配置
        admin_user = load_test_data('_common', 'test_users', 'admin')
        
        # 加载测试环境配置
        host_workspace = load_test_data('ks_core', 'test_environment', 'workspaces.host.name')
        
        # 加载角色测试数据
        roles = load_test_data('ks_core', 'access_management/roles', 'test_roles')
    """
    # 构建文件路径
    if component == '_common':
        data_file = Path(__file__).parent.parent / "data" / "api_data" / "_common" / f"{module}.json"
    else:
        # 处理 module 可能包含子目录的情况，如 "access_management/roles"
        module_path = Path(module)
        # 如果 module 是文件名（没有后缀），且 data_key 为 None，直接使用 {module}.json
        # 如果 module 是目录，且 data_key 为 None，使用 {data_key}.json
        if module_path.suffix == '' and data_key is None:
            # 直接使用 module.json
            data_file = Path(__file__).parent.parent / "data" / "api_data" / component / f"{module}.json"
        else:
            # module 包含子目录或需要 data_key
            data_file = Path(__file__).parent.parent / "data" / "api_data" / component / module_path
    
    try:
        if data_file.exists():
            data = json.loads(data_file.read_text(encoding="utf-8"))
            
            # 如果指定了 data_key，获取对应值
            if data_key:
                # 支持嵌套 key，如 "workspaces.host.name"
                keys = data_key.split('.')
                for key in keys:
                    if isinstance(data, dict):
                        data = data.get(key, default)
                    else:
                        return default
            
            # 替换变量
            if replace_vars:
                data = replace_variables(data)
            
            return data
    except Exception as e:
        print(f"加载测试数据失败: {data_file}, error: {e}")
    
    return default


def get_test_data_list(
    component: str, 
    module: str, 
    data_key: str,
    replace_vars: bool = True
) -> List[Dict]:
    """
    获取测试数据列表
    
    Args:
        component: 组件名称
        module: 模块名称
        data_key: 数据键名
        replace_vars: 是否替换变量
    
    Returns:
        测试数据列表
    """
    return load_test_data(component, module, data_key, [], replace_vars)


def load_raw_data(component: str, module: str, data_key: str = None, default: Any = None) -> Any:
    """
    加载原始数据（不替换变量）
    
    用于查看数据模板
    """
    return load_test_data(component, module, data_key, default, replace_vars=False)
