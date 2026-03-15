# -*- coding:utf-8 -*-
"""测试数据加载公共工具"""
import json
from pathlib import Path
from typing import Any, List, Dict


def load_test_data(component: str, module: str, data_key: str, default: Any = None) -> Any:
    """从JSON文件加载测试数据
    
    Args:
        component: 组件名称，如 "ks_core"
        module: 模块名称，如 "multi_cluster"
        data_key: 数据键名，如 "test_labels"
        default: 默认值
    
    Returns:
        测试数据
    """
    data_file = Path(__file__).parent.parent / "data" / "api_data" / component / f"{module}.json"
    
    try:
        if data_file.exists():
            data = json.loads(data_file.read_text(encoding="utf-8"))
            return data.get(data_key, default)
    except Exception:
        pass
    return default


def get_test_data_list(component: str, module: str, data_key: str) -> List[Dict]:
    """获取测试数据列表
    
    Args:
        component: 组件名称
        module: 模块名称
        data_key: 数据键名
    
    Returns:
        测试数据列表
    """
    return load_test_data(component, module, data_key, [])