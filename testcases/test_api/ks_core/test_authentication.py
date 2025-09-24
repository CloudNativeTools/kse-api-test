# -*- coding:utf-8 -*-
"""
File name : test_authentication.PY
Program IDE : PyCharm
Create file time: 2025/9/23 10:55
File Create By Author : qiaoshilu
"""
import pytest

from apis.ks_core.authentication.apis import OpenidUserinfoAPI


@pytest.mark.ks_core
def test_get_userinfo():
    """测试获取用户列表API"""
    res = OpenidUserinfoAPI().send()

    assert res.response_model.name == "admin"
    assert  res.response_model.email == "admin@example.com"