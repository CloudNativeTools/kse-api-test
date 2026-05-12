"""
邮箱(Email)通知渠道单接口测试
API: ListResourceAPI_1, CreateResourceAPI_1, UpdateResourceAPI_1 (resources="configs")

测试策略：
1. 使用标准资源 default-email-config 贯穿查询、修改接口
2. get_for_test 确保资源存在（查不到就创建，存在则先删除再创建）
3. 创建接口使用固定名称 default-email-config，创建前清理已有资源
4. 通知渠道是 Global 级别，不区分多集群
"""
import pytest
from loguru import logger

from apis.whizard_telemetry.notification.apis import (
    ListResourceAPI_1,
    GetResourceAPI_1,
    CreateResourceAPI_1,
    UpdateResourceAPI_1,
    DeleteResourceAPI_1,
    VerifyAPI_1,
)
from testcases.test_api.whizard_telemetry.notification.base import (
    EMAIL_RECEIVER_NAME,
    get_for_test_email_config,
    get_for_test_email_receiver,
    build_update_body,
    delete_resource_if_exists,
)
from utils.api_helpers import deep_merge
from utils.test_data_helper import load_test_data

EMAIL_CONFIG_NAME = "default-email-config"
EMAIL_SECRET_NAME = "global-email-config-secret"


@pytest.mark.notification
class TestCreateEmailConfig:
    """创建邮箱通知渠道"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_before_create(self):
        delete_resource_if_exists("configs", EMAIL_CONFIG_NAME)
        delete_resource_if_exists("secrets", EMAIL_SECRET_NAME)
        yield

    def test_create_email_config(self):
        """使用固定名称创建邮箱通知配置"""
        secret_body = load_test_data(
            "whizard_telemetry", "notification/email_config", "create_email_secret"
        )
        create_secret = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="secrets"),
            request_body=secret_body,
            enable_schema_validation=False
        )
        secret_res = create_secret.send()
        assert secret_res.cached_response.raw_response.status_code in (200, 201), \
            f"创建 secret 失败，状态码: {secret_res.cached_response.raw_response.status_code}"
        logger.info(f"secret 创建成功: {EMAIL_SECRET_NAME}")

        config_body = load_test_data(
            "whizard_telemetry", "notification/email_config", "create_email_config"
        )
        create_config = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="configs"),
            request_body=config_body,
            enable_schema_validation=False
        )
        res = create_config.send()
        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == EMAIL_CONFIG_NAME
        assert "email" in data.get("spec", {})
        logger.info(f"邮箱配置创建成功: {EMAIL_CONFIG_NAME}")


@pytest.mark.notification
class TestListEmailConfig:
    """查询邮箱通知渠道"""

    def test_list_success(self):
        """正常查询邮箱通知渠道列表"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="configs"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.type = "email"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

@pytest.mark.notification
class TestUpdateEmailConfig:
    """更新邮箱通知渠道 (PUT)"""

    def test_update_email_config(self):
        """修改邮箱通知配置"""
        if not get_for_test_email_config():
            pytest.skip("无法创建标准邮箱配置")

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="configs", name=EMAIL_CONFIG_NAME),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        assert res.cached_response.raw_response.status_code == 200

        current_config = res.cached_response.raw_response.json()

        body = build_update_body(current_config, remove_resource_version=False)
        body["spec"]["email"]["from"] = "qiaoshilu@yunify.com"

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="configs", name=EMAIL_CONFIG_NAME),
            request_body=body,
            enable_schema_validation=False
        )
        update_res = update_api.send()

        assert update_res.cached_response.raw_response.status_code == 200, \
            f"更新失败，状态码: {update_res.cached_response.raw_response.status_code}"

        updated_data = update_res.cached_response.raw_response.json()
        assert updated_data.get("spec", {}).get("email", {}).get("from") == "qiaoshilu@yunify.com", \
            "from 字段应已更新"


@pytest.mark.notification
class TestUpdateEmailSecret:
    """更新邮箱secret"""

    def test_update_email_secret(self):
        if not get_for_test_email_config():
            pytest.skip("无法创建标准邮箱配置")

        get_res = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="secrets", name=EMAIL_SECRET_NAME),
            enable_schema_validation=False,
            response=None
        ).send()
        assert get_res.cached_response.raw_response.status_code == 200

        body = build_update_body(get_res.cached_response.raw_response.json(), remove_resource_version=False)
        patch = load_test_data("whizard_telemetry", "notification/email_config", "update_email_secret")
        body = deep_merge(body, patch)

        update_res = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="secrets", name=EMAIL_SECRET_NAME),
            request_body=body,
            enable_schema_validation=False
        ).send()
        assert update_res.cached_response.raw_response.status_code == 200

        updated = update_res.cached_response.raw_response.json().get("data", {})
        assert "authPassword" in updated
        logger.info(f"邮箱secret更新成功: {EMAIL_SECRET_NAME}")


@pytest.mark.notification
class TestVerifyEmailConfig:
    """验证邮箱通知配置"""

    def test_verify_email_config(self):
        """验证邮箱通知配置"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/email_config", "verify_email_body"
        )

        api = VerifyAPI_1(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 202), \
            f"验证邮箱配置失败，状态码: {res.cached_response.raw_response.status_code}"


@pytest.mark.notification
class TestCreateEmailReceiver:
    """创建邮箱接收者"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_before_create(self):
        delete_resource_if_exists("receivers", EMAIL_RECEIVER_NAME)
        yield

    def test_create_email_receiver(self):
        """创建邮箱接收者"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/email_config", "create_email_receiver"
        )
        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="receivers"),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = create_api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建邮箱接收者失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == EMAIL_RECEIVER_NAME
        assert "email" in data.get("spec", {})
        logger.info(f"邮箱接收者创建成功: {EMAIL_RECEIVER_NAME}")


@pytest.mark.notification
class TestListEmailReceiver:
    """查询邮箱接收者"""

    def test_list_receivers_success(self):
        """正常查询邮箱接收者列表"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="receivers"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.type = "email"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

    def test_list_receivers_with_name_filter(self):
        """按名称过滤 - 查询邮箱接收者"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="receivers"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.name = "email"
        api.query_params.type = "email"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        found = any(
            item.get("metadata", {}).get("name") == EMAIL_RECEIVER_NAME
            for item in (data.get("items") or [])
        )
        assert found, f"邮箱接收者 {EMAIL_RECEIVER_NAME} 应存在于列表中"


@pytest.mark.notification
class TestUpdateEmailReceiver:
    """更新邮箱接收者 (PUT)"""

    def test_update_email_receiver(self):
        """修改邮箱接收者"""
        if not get_for_test_email_receiver():
            pytest.skip("无法创建标准邮箱接收者")

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="receivers", name=EMAIL_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        assert res.cached_response.raw_response.status_code == 200

        current_receiver = res.cached_response.raw_response.json()

        body = build_update_body(current_receiver, remove_resource_version=False)
        patch = load_test_data("whizard_telemetry", "notification/email_config", "update_email_receiver")
        body = deep_merge(body, patch)

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="receivers", name=EMAIL_RECEIVER_NAME),
            request_body=body,
            enable_schema_validation=False
        )
        update_res = update_api.send()

        assert update_res.cached_response.raw_response.status_code == 200, \
            f"更新邮箱接收者失败，状态码: {update_res.cached_response.raw_response.status_code}"

        updated_data = update_res.cached_response.raw_response.json()
        annotations = updated_data.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "alias-test"
        assert annotations.get("kubesphere.io/description") == "desc-test"
        logger.info(f"邮箱接收者更新成功: {EMAIL_RECEIVER_NAME}")


@pytest.mark.notification
class TestDeleteEmailReceiver:
    """删除邮箱接收者"""

    def test_delete_email_receiver(self):
        """删除邮箱接收者"""
        if not get_for_test_email_receiver():
            pytest.skip("无法创建标准邮箱接收者")

        delete_api = DeleteResourceAPI_1(
            path_params=DeleteResourceAPI_1.PathParams(resources="receivers", name=EMAIL_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        )
        delete_res = delete_api.send()

        assert delete_res.cached_response.raw_response.status_code in (200, 204), \
            f"删除邮箱接收者失败，状态码: {delete_res.cached_response.raw_response.status_code}"

        data = delete_res.cached_response.raw_response.json()
        assert data.get("message") == "success"
        logger.info(f"邮箱接收者删除成功: {EMAIL_RECEIVER_NAME}")