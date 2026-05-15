# -*- coding:utf-8 -*-
"""
File name : api_helpers.py.PY
Program IDE : PyCharm
Create file time: 2025/10/11 11:33
File Create By Author : qiaoshilu
"""
import copy


def get_http_info(res):
    """从AoResponse对象中提取底层HTTP响应信息"""
    raw = res.cached_response.raw_response
    return raw.status_code, raw.text


def deep_merge(base: dict, override: dict) -> dict:
    """递归合并 override 到 base，支持嵌套 dict"""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def clean_api_response(current_data: dict, remove_resource_version: bool = True) -> dict:
    """
    清理 API 响应数据，移除只读的系统字段，用于构造 PUT/PATCH 请求体。

    所有 Kubernetes 风格资源的 Update/Patch 操作都需要先 GET 当前数据，
    然后移除以下只读字段再提交：
    - uid, generation, managedFields, creationTimestamp（始终移除）
    - resourceVersion（可选，PATCH 时移除，PUT 时保留用于乐观锁）
    - status（始终移除）

    Args:
        current_data: GET/LIST 接口返回的完整资源数据
        remove_resource_version: 是否移除 resourceVersion（PATCH=True, PUT=False）

    Returns:
        清理后的请求体 dict
    """
    body = copy.deepcopy(current_data)
    metadata = body.get("metadata", {})
    metadata.pop("uid", None)
    metadata.pop("generation", None)
    metadata.pop("managedFields", None)
    metadata.pop("creationTimestamp", None)
    if remove_resource_version:
        metadata.pop("resourceVersion", None)
    body.pop("status", None)
    return body
