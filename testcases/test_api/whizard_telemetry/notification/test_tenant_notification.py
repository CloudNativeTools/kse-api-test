"""
租户侧 Email 通知单接口测试
API: ListResourceAPI, CreateResourceAPI, GetResourceAPI, UpdateResourceAPI, DeleteResourceAPI, VerifyAPI

测试策略：
1. 使用 permission_accounts.json 中所有 9 个租户账号（pl_admin ~ pro_viewer）
2. 每个租户 CRUD 各自独立的 email receiver (/users/{user}/receivers/{name})
3. 验证租户间数据隔离
"""
import json
import pytest
from loguru import logger

from apis.whizard_telemetry.notification.apis import (
    ListResourceAPI,
    CreateResourceAPI,
    GetResourceAPI,
    UpdateResourceAPI,
    DeleteResourceAPI,
    VerifyAPI,
)
from utils.test_data_helper import load_test_data
from utils.user_switch_helper import UserContext
from testcases.test_api.whizard_telemetry.notification.base import build_update_body
from utils.api_helpers import deep_merge

ACCOUNTS = load_test_data("_common", "permission_accounts")
ALL_USERS = list(ACCOUNTS.items())
RECEIVER_TEMPLATE = load_test_data(
    "whizard_telemetry", "notification/tenant_email_config", "receiver_template",
    replace_vars=False
)
VERIFY_TEMPLATE = load_test_data(
    "whizard_telemetry", "notification/tenant_email_config", "verify_receiver_template",
    replace_vars=False
)
UPDATE_ANNOTATIONS = load_test_data(
    "whizard_telemetry", "notification/tenant_email_config", "update_tenant_receiver"
)


def _fill_template(template: dict, username: str) -> dict:
    raw = json.dumps(template)
    return json.loads(raw.replace("{{username}}", username))


def _receiver_name(username: str) -> str:
    return f"{username}-email-receiver"


def _build_receiver(username: str) -> dict:
    return _fill_template(RECEIVER_TEMPLATE, username)


def _build_verify_body(username: str) -> dict:
    return _fill_template(VERIFY_TEMPLATE, username)


def ensure_tenant_receiver(account_key: str) -> bool:
    """确保租户 email receiver 存在，不存在则创建"""
    account = ACCOUNTS[account_key]
    username = account["user"]
    try:
        with UserContext(username, account["pwd"]):
            get_api = GetResourceAPI(
                path_params=GetResourceAPI.PathParams(
                    user=username, resources="receivers", name=_receiver_name(username)
                ),
                enable_schema_validation=False,
                response=None,
            )
            res = get_api.send()
            if res.cached_response.raw_response.status_code == 200:
                return True

            body = _build_receiver(username)
            create_api = CreateResourceAPI(
                path_params=CreateResourceAPI.PathParams(
                    user=username, resources="receivers"
                ),
                request_body=body,
                enable_schema_validation=False,
            )
            create_res = create_api.send()
            return create_res.cached_response.raw_response.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"ensure_tenant_receiver failed for {username}: {e}")
        return False


def delete_tenant_receiver_if_exists(account_key: str) -> None:
    """如果租户 receiver 存在则删除，忽略 404"""
    account = ACCOUNTS[account_key]
    username = account["user"]
    try:
        with UserContext(username, account["pwd"]):
            get_api = GetResourceAPI(
                path_params=GetResourceAPI.PathParams(
                    user=username, resources="receivers", name=_receiver_name(username)
                ),
                enable_schema_validation=False,
                response=None,
            )
            res = get_api.send()
            if res.cached_response.raw_response.status_code != 200:
                return

            delete_api = DeleteResourceAPI(
                path_params=DeleteResourceAPI.PathParams(
                    user=username, resources="receivers", name=_receiver_name(username)
                ),
                enable_schema_validation=False,
                response=None,
            )
            del_res = delete_api.send()
            if del_res.cached_response.raw_response.status_code in (200, 204):
                logger.info(f"已删除租户 receiver: {username}/{_receiver_name(username)}")
    except Exception as e:
        logger.warning(f"delete_tenant_receiver_if_exists failed for {username}: {e}")


@pytest.mark.notification
@pytest.mark.tenant_permission
class TestTenantCreateReceiver:
    """各租户创建自己的 email receiver"""

    @pytest.mark.parametrize(
        "account_key, account", ALL_USERS, ids=[k for k, _ in ALL_USERS]
    )
    def test_create_receiver(self, account_key, account):
        """使用各自用户名创建 email receiver"""
        try:
            delete_tenant_receiver_if_exists(account_key)
        except Exception:
            pass

        with UserContext(account["user"], account["pwd"]):
            body = _build_receiver(account["user"])
            api = CreateResourceAPI(
                path_params=CreateResourceAPI.PathParams(
                    user=account["user"], resources="receivers"
                ),
                request_body=body,
                enable_schema_validation=False,
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code in (
                200,
                201,
            ), f"创建 receiver 失败，状态码: {res.cached_response.raw_response.status_code}"

            data = res.cached_response.raw_response.json()
            assert (
                data.get("metadata", {}).get("name") == _receiver_name(account["user"])
            )
            assert "email" in data.get("spec", {})
            logger.info(
                f"[{account_key}] 租户 receiver 创建成功: {_receiver_name(account['user'])}"
            )


@pytest.mark.notification
@pytest.mark.tenant_permission
class TestTenantListReceivers:
    """各租户查询自己的 receivers 列表"""

    @pytest.mark.parametrize(
        "account_key, account", ALL_USERS, ids=[k for k, _ in ALL_USERS]
    )
    def test_list_receivers(self, account_key, account):
        """列出租户自己的 email receivers"""
        with UserContext(account["user"], account["pwd"]):
            api = ListResourceAPI(
                path_params=ListResourceAPI.PathParams(
                    user=account["user"], resources="receivers"
                ),
                enable_schema_validation=False,
                response=None,
            )
            api.query_params.type = "email"
            api.query_params.limit = "10"
            api.query_params.sortBy = "createTime"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data
            assert "totalItems" in data
            logger.info(f"[{account_key}] 查询 receivers 列表成功")


@pytest.mark.notification
@pytest.mark.tenant_permission
class TestTenantGetReceiver:
    """各租户获取自己的 receiver 详情"""

    @pytest.mark.parametrize(
        "account_key, account", ALL_USERS, ids=[k for k, _ in ALL_USERS]
    )
    def test_get_receiver(self, account_key, account):
        """获取租户自己的 email receiver 详情"""
        if not ensure_tenant_receiver(account_key):
            pytest.skip(f"无法为 {account['user']} 准备 receiver")

        with UserContext(account["user"], account["pwd"]):
            api = GetResourceAPI(
                path_params=GetResourceAPI.PathParams(
                    user=account["user"],
                    resources="receivers",
                    name=_receiver_name(account["user"]),
                ),
                enable_schema_validation=False,
                response=None,
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert data.get("metadata", {}).get("name") == _receiver_name(
                account["user"]
            )
            assert "email" in data.get("spec", {})
            logger.info(
                f"[{account_key}] 获取 receiver 详情成功: {_receiver_name(account['user'])}"
            )


@pytest.mark.notification
@pytest.mark.tenant_permission
class TestTenantUpdateReceiver:
    """各租户更新自己的 receiver (PUT)"""

    @pytest.mark.parametrize(
        "account_key, account", ALL_USERS, ids=[k for k, _ in ALL_USERS]
    )
    def test_update_receiver(self, account_key, account):
        """更新租户自己的 email receiver"""
        if not ensure_tenant_receiver(account_key):
            pytest.skip(f"无法为 {account['user']} 准备 receiver")

        with UserContext(account["user"], account["pwd"]):
            get_api = GetResourceAPI(
                path_params=GetResourceAPI.PathParams(
                    user=account["user"],
                    resources="receivers",
                    name=_receiver_name(account["user"]),
                ),
                enable_schema_validation=False,
                response=None,
            )
            get_res = get_api.send()
            assert get_res.cached_response.raw_response.status_code == 200

            current = get_res.cached_response.raw_response.json()
            body = build_update_body(current, remove_resource_version=False)
            body = deep_merge(body, UPDATE_ANNOTATIONS)

            update_api = UpdateResourceAPI(
                path_params=UpdateResourceAPI.PathParams(
                    user=account["user"],
                    resources="receivers",
                    name=_receiver_name(account["user"]),
                ),
                request_body=body,
                enable_schema_validation=False,
            )
            update_res = update_api.send()
            assert update_res.cached_response.raw_response.status_code == 200, (
                f"更新 receiver 失败，状态码: "
                f"{update_res.cached_response.raw_response.status_code}"
            )

            updated = update_res.cached_response.raw_response.json()
            annotations = updated.get("metadata", {}).get("annotations", {})
            assert annotations.get("kubesphere.io/alias-name") == "tenant-alias-test"
            assert annotations.get("kubesphere.io/description") == "tenant-desc-test"
            logger.info(f"[{account_key}] 更新 receiver 成功")


@pytest.mark.notification
@pytest.mark.tenant_permission
class TestTenantVerifyReceiver:
    """各租户验证通知"""

    @pytest.mark.parametrize(
        "account_key, account", ALL_USERS, ids=[k for k, _ in ALL_USERS]
    )
    def test_verify_receiver(self, account_key, account):
        """验证租户通知配置"""
        if not ensure_tenant_receiver(account_key):
            pytest.skip(f"无法为 {account['user']} 准备 receiver")

        with UserContext(account["user"], account["pwd"]):
            body = _build_verify_body(account["user"])
            api = VerifyAPI(
                path_params=VerifyAPI.PathParams(user=account["user"]),
                request_body=body,
                enable_schema_validation=False,
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code in (
                200,
                202,
            ), f"验证失败，状态码: {res.cached_response.raw_response.status_code}"
            logger.info(f"[{account_key}] 验证通知成功")


@pytest.mark.notification
@pytest.mark.tenant_permission
class TestTenantDeleteReceiver:
    """各租户删除自己的 receiver"""

    @pytest.mark.parametrize(
        "account_key, account", ALL_USERS, ids=[k for k, _ in ALL_USERS]
    )
    def test_delete_receiver(self, account_key, account):
        """删除租户自己的 email receiver"""
        if not ensure_tenant_receiver(account_key):
            pytest.skip(f"无法为 {account['user']} 准备 receiver")

        with UserContext(account["user"], account["pwd"]):
            api = DeleteResourceAPI(
                path_params=DeleteResourceAPI.PathParams(
                    user=account["user"],
                    resources="receivers",
                    name=_receiver_name(account["user"]),
                ),
                enable_schema_validation=False,
                response=None,
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code in (
                200,
                204,
            ), f"删除 receiver 失败，状态码: {res.cached_response.raw_response.status_code}"

            data = res.cached_response.raw_response.json()
            assert data.get("message") == "success"
            logger.info(
                f"[{account_key}] 删除 receiver 成功: {_receiver_name(account['user'])}"
            )


@pytest.mark.notification
@pytest.mark.tenant_permission
class TestTenantReceiverIsolation:
    """租户间 receiver 数据隔离验证"""

    ISOLATION_PAIRS = [
        ("ws_admin", "pro_admin"),
        ("ws_viewer", "pro_admin"),
        ("pro_admin", "ws_admin"),
        ("pro_operator", "pro_admin"),
    ]

    @pytest.mark.parametrize(
        "attacker_key, victim_key", ISOLATION_PAIRS, ids=[f"{a}_tries_{v}" for a, v in ISOLATION_PAIRS]
    )
    def test_cross_tenant_get_denied(self, attacker_key, victim_key):
        """租户 A 无法获取租户 B 的 receiver（应返回 403）"""
        victim = ACCOUNTS[victim_key]
        attacker = ACCOUNTS[attacker_key]

        if not ensure_tenant_receiver(victim_key):
            pytest.skip(f"无法为 {victim['user']} 准备 receiver")

        with UserContext(attacker["user"], attacker["pwd"]):
            api = GetResourceAPI(
                path_params=GetResourceAPI.PathParams(
                    user=victim["user"],
                    resources="receivers",
                    name=_receiver_name(victim["user"]),
                ),
                enable_schema_validation=False,
                response=None,
            )
            res = api.send()
            assert (
                res.cached_response.raw_response.status_code == 403
            ), f"预期 403，实际 {res.cached_response.raw_response.status_code}"
            logger.info(
                f"[{attacker_key}] 越权访问 [{victim_key}] receiver 被拒绝 (403)"
            )

    @pytest.mark.parametrize(
        "attacker_key, victim_key", ISOLATION_PAIRS, ids=[f"{a}_del_{v}" for a, v in ISOLATION_PAIRS]
    )
    def test_cross_tenant_delete_denied(self, attacker_key, victim_key):
        """租户 A 无法删除租户 B 的 receiver（应返回 403）"""
        victim = ACCOUNTS[victim_key]
        attacker = ACCOUNTS[attacker_key]

        if not ensure_tenant_receiver(victim_key):
            pytest.skip(f"无法为 {victim['user']} 准备 receiver")

        with UserContext(attacker["user"], attacker["pwd"]):
            api = DeleteResourceAPI(
                path_params=DeleteResourceAPI.PathParams(
                    user=victim["user"],
                    resources="receivers",
                    name=_receiver_name(victim["user"]),
                ),
                enable_schema_validation=False,
                response=None,
            )
            res = api.send()
            assert (
                res.cached_response.raw_response.status_code == 403
            ), f"预期 403，实际 {res.cached_response.raw_response.status_code}"
            logger.info(
                f"[{attacker_key}] 越权删除 [{victim_key}] receiver 被拒绝 (403)"
            )

    def test_plat_admin_can_access_any(self):
        """平台管理员 pl-admin 可以访问任意租户的 receiver"""
        victim = ACCOUNTS["pro_admin"]
        attacker = ACCOUNTS["pl_admin"]

        if not ensure_tenant_receiver("pro_admin"):
            pytest.skip("无法为 pro_admin 准备 receiver")

        with UserContext(attacker["user"], attacker["pwd"]):
            api = GetResourceAPI(
                path_params=GetResourceAPI.PathParams(
                    user=victim["user"],
                    resources="receivers",
                    name=_receiver_name(victim["user"]),
                ),
                enable_schema_validation=False,
                response=None,
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200, (
                f"pl-admin 应能访问 pro-admin 的 receiver，"
                f"实际状态码: {res.cached_response.raw_response.status_code}"
            )
            logger.info("平台管理员 pl-admin 可访问任意租户 receiver (200)")