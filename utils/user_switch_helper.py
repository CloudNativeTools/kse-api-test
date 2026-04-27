# -*- coding:utf-8 -*-
"""
多账号切换工具
提供 UserContext 上下文管理器，用于在不同账号间切换
"""
from typing import Optional
from aomaker.core.http_client import HTTPClient
from aomaker.storage import cache
from apis.ks_core.authentication.apis import OpenidTokenAPI


def get_token_for_user(username: str, password: str) -> str:
    """
    用指定账号登录获取 token

    Args:
        username: 用户名
        password: 密码

    Returns:
        str: access_token
    """
    login_api = OpenidTokenAPI(
        request_body=OpenidTokenAPI.RequestBodyModel(
            grant_type="password",
            username=username,
            password=password,
            client_id="kubesphere",
            client_secret="kubesphere"
        ),
        http_client=HTTPClient()
    )
    resp = login_api.send()
    return resp.response_model.access_token


def switch_to_user(username: str, password: str):
    """
    切换到指定用户（覆盖 cache headers 和 HTTPClient session headers）

    Args:
        username: 用户名
        password: 密码
    """
    token = get_token_for_user(username, password)
    cache.del_by_condition(where={"var_name": "headers"})
    cache.set('headers', {'Authorization': f'Bearer {token}'})
    from aomaker.core.http_client import get_http_client
    http_client = get_http_client()
    http_client.session.headers.update({'Authorization': f'Bearer {token}'})


def get_current_headers() -> Optional[dict]:
    """获取当前 headers"""
    return cache.get('headers')


def switch_to_admin():
    """切换回 admin 账号（从 config 读取）"""
    from aomaker.config_handlers import EnvVars
    env_vars = EnvVars()
    account = env_vars.current_env_conf.get('account', {})
    switch_to_user(account.get('user'), account.get('pwd'))


class UserContext:
    """
    用户上下文管理器，切换到指定账号执行操作后自动恢复

    用法:
        with UserContext("ws_admin", "password"):
            # 以 ws_admin 身份调用 API
            res = SomeAPI().send()
        # 退出后自动恢复到之前的账号

    Args:
        username: 用户名
        password: 密码
        save_restore: 是否保存恢复信息，默认 True
    """

    def __init__(self, username: str, password: str, save_restore: bool = True):
        self.username = username
        self.password = password
        self.save_restore = save_restore
        self._original_headers: Optional[dict] = None

    def __enter__(self):
        if self.save_restore:
            self._original_headers = cache.get('headers')
        switch_to_user(self.username, self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.save_restore and self._original_headers is not None:
            cache.del_by_condition(where={"var_name": "headers"})
            cache.set('headers', self._original_headers)
            from aomaker.core.http_client import get_http_client
            http_client = get_http_client()
            original_auth = self._original_headers.get('Authorization', '')
            http_client.session.headers.update({'Authorization': original_auth})
        return False
