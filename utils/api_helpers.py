# -*- coding:utf-8 -*-
"""
File name : api_helpers.py.PY
Program IDE : PyCharm
Create file time: 2025/10/11 11:33
File Create By Author : qiaoshilu
"""


def get_http_info(res):
    """从AoResponse对象中提取底层HTTP响应信息"""
    raw = res.cached_response.raw_response
    return raw.status_code, raw.text
