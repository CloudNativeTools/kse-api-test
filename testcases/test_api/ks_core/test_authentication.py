# -*- coding:utf-8 -*-
"""
File name : test_authentication.PY
Program IDE : PyCharm
Create file time: 2025/9/23 10:55
File Create By Author : qiaoshilu
"""
import json

import pytest

from apis.ks_core.authentication.apis import OpenidUserinfoAPI, OpenidKeysAPI
from utils.api_helpers import get_http_info


@pytest.fixture
def invalid_token():
    # 模拟非法token
    return "Bearer invalid_token_example"


@pytest.fixture
def expired_token():
    # 模拟过期token
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8va3MtY29uc29sZS5rdWJlc3BoZXJlLXN5c3RlbS5zdmM6MzA4ODAiLCJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MDE1NTcxNCwiaWF0IjoxNzYwMTQ4NTE0LCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwidXNlcm5hbWUiOiJhZG1pbiJ9.qd2d1qxB4WE9sNN2hNvgI9QxFWJhQekYa7dMGw3Ekns"


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
    assert any(w in text.lower() for w in ["expired", "unauthorized", "failure"])


@pytest.mark.test
def test_get_oauth_keys_success():
    """测试获取公钥列表（/oauth/keys）"""
    api = OpenidKeysAPI(enable_schema_validation=False)
    res = api.send()

    key = res.response_model.keys[0]

    assert key.use == "sig", "use 应为 'sig'"
    assert key.kty == "RSA", "kty 应为 'RSA'"
    assert key.alg == "RS256", "alg 应为 'RS256'"