"""
通知渠道配置场景测试 - 邮箱完整工作流
流程：创建Secret -> 创建Config -> 创建Receiver -> 验证 -> 更新Config -> 更新Receiver -> 查看
"""
import pytest
from loguru import logger

from apis.whizard_telemetry.notification.apis import (
    GetResourceAPI_1,
    CreateResourceAPI_1,
    UpdateResourceAPI_1,
    VerifyAPI_1,
)
from testcases.test_api.whizard_telemetry.notification.base import (
    EMAIL_CONFIG_NAME,
    EMAIL_SECRET_NAME,
    EMAIL_RECEIVER_NAME,
    build_update_body,
    delete_resource_if_exists,
)
from utils.api_helpers import deep_merge
from utils.test_data_helper import load_test_data


@pytest.mark.notification_scene
class TestEmailChannelConfigScenario:
    """邮箱通知渠道场景测试 - 完整工作流"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_before_scenario(self):
        delete_resource_if_exists("secrets", EMAIL_SECRET_NAME)
        delete_resource_if_exists("configs", EMAIL_CONFIG_NAME)
        delete_resource_if_exists("receivers", EMAIL_RECEIVER_NAME)
        yield

    def test_01_create_secret(self):
        """创建邮箱 Secret"""
        body = load_test_data(
            "whizard_telemetry", "notification/email_config", "create_email_secret"
        )
        api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="secrets"),
            request_body=body,
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code in (200, 201)
        logger.info("1. 邮箱 Secret 创建成功")

    def test_02_create_config(self):
        """创建邮箱 Config"""
        body = load_test_data(
            "whizard_telemetry", "notification/email_config", "create_email_config"
        )
        api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="configs"),
            request_body=body,
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code in (200, 201)
        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == EMAIL_CONFIG_NAME
        assert "email" in data.get("spec", {})
        logger.info("2. 邮箱 Config 创建成功")

    def test_03_create_receiver(self):
        """创建邮箱 Receiver"""
        body = load_test_data(
            "whizard_telemetry", "notification/email_config", "create_email_receiver"
        )
        api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="receivers"),
            request_body=body,
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code in (200, 201)
        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == EMAIL_RECEIVER_NAME
        assert "email" in data.get("spec", {})
        logger.info("3. 邮箱 Receiver 创建成功")

    def test_04_verify_config(self):
        """验证邮箱通知配置"""
        body = load_test_data(
            "whizard_telemetry", "notification/email_config", "verify_email_body"
        )
        api = VerifyAPI_1(
            request_body=body,
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code in (200, 202)
        logger.info("4. 邮箱配置验证成功")

    def test_05_update_config(self):
        """更新邮箱 Config (PUT)"""
        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="configs", name=EMAIL_CONFIG_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code == 200

        current = get_res.cached_response.raw_response.json()
        put_body = build_update_body(current, remove_resource_version=False)
        put_body["spec"]["email"]["from"] = "qiaoshilu@yunify.com"

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="configs", name=EMAIL_CONFIG_NAME),
            request_body=put_body,
            enable_schema_validation=False
        )
        update_res = update_api.send()
        assert update_res.cached_response.raw_response.status_code == 200
        updated = update_res.cached_response.raw_response.json()
        assert updated.get("spec", {}).get("email", {}).get("from") == "qiaoshilu@yunify.com"
        logger.info("5. 邮箱 Config 更新成功")

    def test_06_update_receiver(self):
        """更新邮箱 Receiver (PUT)"""
        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="receivers", name=EMAIL_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code == 200

        current = get_res.cached_response.raw_response.json()
        put_body = build_update_body(current, remove_resource_version=False)
        patch = load_test_data("whizard_telemetry", "notification/email_config", "update_email_receiver")
        put_body = deep_merge(put_body, patch)

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="receivers", name=EMAIL_RECEIVER_NAME),
            request_body=put_body,
            enable_schema_validation=False
        )
        update_res = update_api.send()
        assert update_res.cached_response.raw_response.status_code == 200
        updated = update_res.cached_response.raw_response.json()
        annotations = updated.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "alias-test"
        assert annotations.get("kubesphere.io/description") == "desc-test"
        logger.info("6. 邮箱 Receiver 更新成功")

    def test_07_get_and_verify(self):
        """查看更新结果"""
        get_config = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="configs", name=EMAIL_CONFIG_NAME),
            enable_schema_validation=False,
            response=None
        )
        config_res = get_config.send()
        assert config_res.cached_response.raw_response.status_code == 200
        config_data = config_res.cached_response.raw_response.json()
        assert config_data.get("spec", {}).get("email", {}).get("from") == "qiaoshilu@yunify.com"

        get_receiver = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="receivers", name=EMAIL_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        )
        receiver_res = get_receiver.send()
        assert receiver_res.cached_response.raw_response.status_code == 200
        receiver_data = receiver_res.cached_response.raw_response.json()
        annotations = receiver_data.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "alias-test"
        assert annotations.get("kubesphere.io/description") == "desc-test"
        logger.info("7. 更新结果验证成功")

    