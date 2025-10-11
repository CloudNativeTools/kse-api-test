# -*- coding:utf-8 -*-
"""
File name : test_authentication.PY
Program IDE : PyCharm
Create file time: 2025/9/23 10:55
File Create By Author : qiaoshilu
"""
import json

import pytest

from apis.ks_core.authentication.apis import OpenidUserinfoAPI
from utils.api_helpers import get_http_info


@pytest.fixture
def invalid_token():
    # 模拟非法token
    return "Bearer invalid_token_example"


@pytest.fixture
def expired_token():
    # 模拟过期token
    return "Bearer expired_token_example"


@pytest.mark.authentication
def test_get_userinfo():
    """获取用户信息"""
    res = OpenidUserinfoAPI().send()

    assert res.response_model.sub == "admin"
    assert res.response_model.name == "admin"
    assert res.response_model.email == "admin@example.com"
    assert res.response_model.preferred_username == "admin"


@pytest.mark.authentication
def test_get_userinfo_invalid_token(invalid_token):
    """无效token"""
    api = OpenidUserinfoAPI(enable_schema_validation=False)
    api.headers["Authorization"] = invalid_token
    res = api.send()

    status, text = get_http_info(res)
    assert status == 401, f"expected 401, got {status}, body: {text}"
    assert any(w in text.lower() for w in ["invalid", "unauthorized", "failure"])


@pytest.mark.authentication
def test_get_userinfo_no_token():
    """缺少token"""
    api = OpenidUserinfoAPI(enable_schema_validation=False)
    api.headers["Authorization"] = ""
    res = api.send()

    status, text = get_http_info(res)
    if text.startswith('"') and text.endswith('"'):
        text = json.loads(text)  # 去掉外层引号

    assert status == 401, f"expected 401, got {status}, body: {text}"
    assert text == "login_required"


@pytest.mark.authentication
def test_get_userinfo_expired_token(expired_token):
    """过期token"""
    api = OpenidUserinfoAPI(enable_schema_validation=False)
    api.headers["Authorization"] = expired_token
    res = api.send()

    status, text = get_http_info(res)
    assert status == 401, f"expected 401, got {status}, body: {text}"
    assert any(w in text.lower() for w in ["unauthorized", "failure"])
