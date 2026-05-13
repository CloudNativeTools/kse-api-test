"""
钉钉(DingTalk)通知渠道单接口测试
API: ListResourceAPI_1, CreateResourceAPI_1, UpdateResourceAPI_1, VerifyAPI_1

测试策略：
1. 使用标准资源 default-dingtalk-config / global-dingtalk-receiver 贯穿查询、修改接口
2. get_for_test 确保资源存在（查不到就创建）
3. 创建接口单独测试（创建新资源）
4. 通知渠道是 Global 级别，不区分多集群
"""
import pytest
from loguru import logger

from apis.whizard_telemetry.notification.apis import (
    ListResourceAPI_1,
    GetResourceAPI_1,
    CreateResourceAPI_1,
    UpdateResourceAPI_1,
    VerifyAPI_1,
)
from testcases.test_api.whizard_telemetry.notification.base import (
    DINGTALK_CONFIG_NAME,
    DINGTALK_RECEIVER_NAME,
    DINGTALK_SECRET_NAME,
    get_for_test_dingtalk_config,
    get_for_test_dingtalk_receiver,
    build_update_body,
    delete_resource_if_exists,
)
from utils.api_helpers import deep_merge
from utils.test_data_helper import load_test_data


@pytest.mark.notification
class TestListDingtalkConfig:
    """查询钉钉通知渠道"""

    def test_list_configs_success(self):
        """正常查询钉钉通知渠道列表"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="configs"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.type = "dingtalk"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data
        items = data.get("items") or []
        for item in items:
            assert "dingtalk" in item.get("spec", {}), f"非钉钉配置: {item.get('metadata', {}).get('name')}"


@pytest.mark.notification
class TestListDingtalkReceiver:
    """查询钉钉接收方"""

    def test_list_receivers_with_name_filter(self):
        """按名称过滤 - 查询钉钉接收方"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="receivers"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.name = DINGTALK_RECEIVER_NAME
        api.query_params.type = "dingtalk"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        found = any(
            item.get("metadata", {}).get("name") == DINGTALK_RECEIVER_NAME
            for item in (data.get("items") or [])
        )
        assert found, f"钉钉接收方 {DINGTALK_RECEIVER_NAME} 应存在于列表中"


@pytest.mark.notification
class TestCreateDingtalkConfig:
    """创建钉钉通知渠道"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_before_create(self):
        delete_resource_if_exists("configs", DINGTALK_CONFIG_NAME)
        delete_resource_if_exists("receivers", DINGTALK_RECEIVER_NAME)
        delete_resource_if_exists("secrets", DINGTALK_SECRET_NAME)
        yield

    def test_create_dingtalk_config(self):
        """创建钉钉通知配置"""
        secret_body = load_test_data(
            "whizard_telemetry", "notification/dingtalk_config", "create_dingtalk_secret"
        )
        create_secret = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="secrets"),
            request_body=secret_body,
            enable_schema_validation=False
        )
        secret_res = create_secret.send()
        assert secret_res.cached_response.raw_response.status_code in (200, 201), \
            f"创建 secret 失败，状态码: {secret_res.cached_response.raw_response.status_code}"
        logger.info(f"secret 创建成功: {DINGTALK_SECRET_NAME}")

        config_body = load_test_data(
            "whizard_telemetry", "notification/dingtalk_config", "create_dingtalk_config"
        )
        create_config = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="configs"),
            request_body=config_body,
            enable_schema_validation=False
        )
        res = create_config.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建钉钉配置失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == DINGTALK_CONFIG_NAME
        assert "dingtalk" in data.get("spec", {})

    def test_create_dingtalk_receiver(self):
        """创建钉钉接收方"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/dingtalk_config", "create_dingtalk_receiver"
        )
        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="receivers"),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = create_api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建钉钉接收方失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == DINGTALK_RECEIVER_NAME
        assert "dingtalk" in data.get("spec", {})
        logger.info(f"钉钉接收方创建成功: {DINGTALK_RECEIVER_NAME}")


@pytest.mark.notification
class TestVerifyDingtalkConfig:
    """验证钉钉通知配置"""

    def test_verify_dingtalk_config(self):
        """验证钉钉通知配置（会话方式）"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/dingtalk_config", "verify_dingtalk_body"
        )

        api = VerifyAPI_1(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 202), \
            f"验证钉钉配置失败，状态码: {res.cached_response.raw_response.status_code}"


@pytest.mark.notification
class TestUpdateDingtalkConfig:
    """更新钉钉通知渠道 (PUT)"""

    def test_update_dingtalk_config(self):
        """修改钉钉通知配置"""
        if not get_for_test_dingtalk_config():
            pytest.skip("无法创建钉钉配置")

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="configs", name=DINGTALK_CONFIG_NAME),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        assert res.cached_response.raw_response.status_code == 200

        current_config = res.cached_response.raw_response.json()

        body = build_update_body(current_config, remove_resource_version=False)
        body.setdefault("metadata", {}).setdefault("annotations", {})["kubesphere.io/alias-name"] = "updated-dingtalk-config"

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="configs", name=DINGTALK_CONFIG_NAME),
            request_body=body,
            enable_schema_validation=False
        )
        update_res = update_api.send()

        assert update_res.cached_response.raw_response.status_code == 200, \
            f"更新钉钉配置失败，状态码: {update_res.cached_response.raw_response.status_code}"

        updated_data = update_res.cached_response.raw_response.json()
        annotations = updated_data.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "updated-dingtalk-config", \
            "注解应已更新"


@pytest.mark.notification
class TestUpdateDingtalkReceiver:
    """更新钉钉接收方 (PUT)"""

    def test_update_dingtalk_receiver(self):
        """修改钉钉接收方"""
        if not get_for_test_dingtalk_receiver():
            pytest.skip("无法创建标准钉钉接收方")

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="receivers", name=DINGTALK_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_api.query_params.type = "dingtalk"
        res = get_api.send()
        assert res.cached_response.raw_response.status_code == 200

        current_receiver = res.cached_response.raw_response.json()

        body = build_update_body(current_receiver, remove_resource_version=False)
        body["spec"]["dingtalk"]["enabled"] = False

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="receivers", name=DINGTALK_RECEIVER_NAME),
            request_body=body,
            enable_schema_validation=False
        )
        update_res = update_api.send()

        assert update_res.cached_response.raw_response.status_code == 200, \
            f"更新钉钉接收方失败，状态码: {update_res.cached_response.raw_response.status_code}"

        updated_data = update_res.cached_response.raw_response.json()
        updated_dingtalk = updated_data.get("spec", {}).get("dingtalk", {})
        assert updated_dingtalk.get("enabled") is False, "enabled 应已禁用"


@pytest.mark.notification
class TestVerifyDingtalkWebhook:
    """验证钉钉通知配置 - webhook接收者"""

    def test_verify_dingtalk_webhook(self):
        """验证钉钉通知配置（含chatbot webhook）"""
        if not get_for_test_dingtalk_config():
            pytest.skip("无法创建钉钉配置")

        request_body = load_test_data(
            "whizard_telemetry", "notification/dingtalk_config", "verify_dingtalk_webhook_body"
        )

        api = VerifyAPI_1(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 202), \
            f"验证钉钉webhook配置失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("Status") == 200
        assert "successfully" in data.get("Message", "").lower()


@pytest.mark.notification
class TestUpdateDingtalkSecretWebhook:
    """更新钉钉secret - 补充webhook和chatbotsecret"""

    def test_update_dingtalk_secret_webhook(self):
        if not get_for_test_dingtalk_config():
            pytest.skip("无法创建钉钉配置")

        get_res = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="secrets", name=DINGTALK_SECRET_NAME),
            enable_schema_validation=False,
            response=None
        ).send()
        assert get_res.cached_response.raw_response.status_code == 200

        body = build_update_body(get_res.cached_response.raw_response.json(), remove_resource_version=False)
        patch = load_test_data("whizard_telemetry", "notification/dingtalk_config", "update_secret_webhook")
        body = deep_merge(body, patch)

        update_res = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="secrets", name=DINGTALK_SECRET_NAME),
            request_body=body,
            enable_schema_validation=False
        ).send()
        assert update_res.cached_response.raw_response.status_code == 200

        updated = update_res.cached_response.raw_response.json().get("data", {})
        assert "webhook" in updated
        assert "chatbotsecret" in updated
        assert "appkey" in updated
        assert "appsecret" in updated
        logger.info(f"钉钉secret更新成功: {DINGTALK_SECRET_NAME}")


@pytest.mark.notification
class TestUpdateDingtalkReceiverWebhook:
    """更新钉钉接收方 - 配置webhook接收者"""

    def test_update_dingtalk_receiver_webhook(self):
        if not get_for_test_dingtalk_receiver():
            pytest.skip("无法创建标准钉钉接收方")

        get_res = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="receivers", name=DINGTALK_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        ).send()
        assert get_res.cached_response.raw_response.status_code == 200

        body = build_update_body(get_res.cached_response.raw_response.json(), remove_resource_version=False)
        patch = load_test_data("whizard_telemetry", "notification/dingtalk_config", "update_receiver_webhook")
        body = deep_merge(body, patch)

        update_res = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="receivers", name=DINGTALK_RECEIVER_NAME),
            request_body=body,
            enable_schema_validation=False
        ).send()
        assert update_res.cached_response.raw_response.status_code == 200

        updated_dingtalk = update_res.cached_response.raw_response.json().get("spec", {}).get("dingtalk", {})
        assert updated_dingtalk.get("enabled") is False, "enabled 应已禁用"
        assert "chatbot" in updated_dingtalk
        assert "webhook" in updated_dingtalk.get("chatbot", {})
        assert "secret" in updated_dingtalk.get("chatbot", {})