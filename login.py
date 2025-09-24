from typing import Union

from aomaker.core.http_client import HTTPClient
from aomaker.session import BaseLogin

from apis.ks_core.authentication.apis import OpenidTokenAPI


class Login(BaseLogin):

    def login(self) -> Union[dict, str]:
        login_request_data = OpenidTokenAPI.RequestBodyModel(
            grant_type="password",
            username=self.account['user'],
            password=self.account['pwd'],
            client_id="kubesphere",
            client_secret="kubesphere"
        )
        login_api = OpenidTokenAPI(
            request_body=login_request_data,
            http_client=HTTPClient()
        )
        resp_login = login_api.send()
        return resp_login.response_model.access_token

    def make_headers(self, resp_login: Union[dict, str]) -> dict:
        token = resp_login
        headers = {
            'Authorization': f"Bearer {token}"
        }
        return headers
