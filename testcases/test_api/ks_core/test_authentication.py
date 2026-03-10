# -*- coding:utf-8 -*-
"""
File name : test_authentication.PY
Program IDE : PyCharm
Create file time: 2025/9/23 10:55
File Create By Author : qiaoshilu
"""
import json

import pytest

from apis.ks_core.authentication.apis import OpenidUserinfoAPI, OpenidKeysAPI, GenerateTOTPAuthKeyAPI, LogoutAPI
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


@pytest.mark.authentication
def test_get_oauth_keys_success():
    """测试获取公钥列表（/oauth/keys）"""
    api = OpenidKeysAPI(enable_schema_validation=False)
    res = api.send()

    key = res.response_model.keys[0]

    assert key.use == "sig", "use 应为 'sig'"
    assert key.kty == "RSA", "kty 应为 'RSA'"
    assert key.alg == "RS256", "alg 应为 'RS256'"


@pytest.mark.authentication
def test_get_user_authkey_success():
    """测试获取指定用户 authkey (/kapis/iam.kubesphere.io/v1beta1/users/{user}/authkey)"""

    # 假设 admin 是存在的用户
    path_params = GenerateTOTPAuthKeyAPI.PathParams(user="admin")
    api = GenerateTOTPAuthKeyAPI(path_params=path_params)

    res = api.send()

    auth_key = res.response_model.authKey

    # 校验 authKey 格式
    assert auth_key.startswith("otpauth://totp/"), f"authKey 格式不正确: {auth_key}"
    assert "issuer=" in auth_key and "secret=" in auth_key, f"authKey 缺少必要参数: {auth_key}"


@pytest.mark.todo
@pytest.mark.authentication
def test_post_user_authkey_todo():
    """[TODO] 测试post用户 authkey 接口 (/kapis/iam.kubesphere.io/v1beta1/users/{user}/authkey)

    说明：
    - 涉及第三方依赖，目前暂不执行。
    """
    pytest.skip("接口依赖外部服务，后续补充实现")


@pytest.mark.todo
@pytest.mark.authentication
def test_delete_user_authkey_todo():
    """[TODO] 测试delete用户 authkey 接口 (/kapis/iam.kubesphere.io/v1beta1/users/{user}/authkey)

    说明：
    - 涉及第三方依赖，目前暂不执行。
    """
    pytest.skip("接口依赖外部服务，后续补充实现")


@pytest.mark.todo
@pytest.mark.authentication
def test_get_authorize_todo():
    """[TODO] 测试获取用户 authorize 接口 (/oauth/authorize)

    说明：
    - 涉及第三方依赖，目前暂不执行。
    """
    pytest.skip("接口依赖外部服务，后续补充实现")


@pytest.mark.todo
@pytest.mark.authentication
def test_post_authorize_todo():
    """[TODO] 测试post用户 authorize 接口 (/oauth/authorize)

    说明：
    - 涉及第三方依赖，目前暂不执行。
    """
    pytest.skip("接口依赖外部服务，后续补充实现")


@pytest.mark.todo
@pytest.mark.authentication
def test_get_callback_todo():
    """ 测试获取oauth callback 接口 (/oauth/callback/{callback})

    说明：
    - 涉及第三方依赖，目前暂不执行。
    """
    pytest.skip("接口依赖外部服务，后续补充实现")


@pytest.mark.test
def test_logout_success():
    """测试退出登录成功 (/oauth/logout)"""

    # 实例化接口对象
    api = LogoutAPI()

    res = api.send()
    status, text = get_http_info(res)

    # 基础断言
    assert status == 200, f"expected 200, got {status}, body: {text}"

    data = json.loads(text)
    assert data["message"] == "success", f"退出登录失败，返回内容: {data}"

