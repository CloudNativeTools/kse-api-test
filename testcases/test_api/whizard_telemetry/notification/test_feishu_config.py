"""
飞书(Feishu)通知渠道单接口测试
API: ListResourceAPI_1, CreateResourceAPI_1, UpdateResourceAPI_1, VerifyAPI_1

测试策略：
1. 使用标准资源 default-feishu-config / global-feishu-receiver 贯穿查询、修改接口
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
    FEISHU_CONFIG_NAME,
    FEISHU_RECEIVER_NAME,
    get_for_test_feishu_config,
    get_for_test_feishu_receiver,
    build_update_body,
    delete_resource_if_exists,
    FEISHU_SECRET_NAME,
)
from utils.test_data_helper import load_test_data

@pytest.mark.notification
class TestListFeishuConfig:
    """查询飞书通知渠道"""

    def test_list_configs_success(self):
        """正常查询飞书通知渠道列表"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="configs"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.type = "feishu"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data
        items = data.get("items") or []
        for item in items:
            assert "feishu" in item.get("spec", {}), f"非飞书配置: {item.get('metadata', {}).get('name')}"


@pytest.mark.notification
class TestListFeishuReceiver:
    """查询飞书接收方"""

    def test_list_receivers_with_name_filter(self):
        """按名称过滤 - 查询飞书接收方"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="receivers"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.name = FEISHU_RECEIVER_NAME
        api.query_params.type = "feishu"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        found = any(
            item.get("metadata", {}).get("name") == FEISHU_RECEIVER_NAME
            for item in (data.get("items") or [])
        )
        assert found, f"飞书接收方 {FEISHU_RECEIVER_NAME} 应存在于列表中"


@pytest.mark.notification
class TestCreateFeishuConfig:
    """创建飞书通知渠道"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_before_create(self):
        delete_resource_if_exists("configs", FEISHU_CONFIG_NAME)
        delete_resource_if_exists("receivers", FEISHU_RECEIVER_NAME)
        delete_resource_if_exists("secrets", FEISHU_SECRET_NAME)
        yield

    def test_create_feishu_config(self):
        """创建飞书通知配置"""
        secret_body = load_test_data(
            "whizard_telemetry", "notification/feishu_config", "create_feishu_secret"
        )
        create_secret = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="secrets"),
            request_body=secret_body,
            enable_schema_validation=False
        )
        secret_res = create_secret.send()
        assert secret_res.cached_response.raw_response.status_code in (200, 201), \
            f"创建 secret 失败，状态码: {secret_res.cached_response.raw_response.status_code}"
        logger.info(f"secret 创建成功: {FEISHU_SECRET_NAME}")

        config_body = load_test_data(
            "whizard_telemetry", "notification/feishu_config", "create_feishu_config"
        )
        create_config = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="configs"),
            request_body=config_body,
            enable_schema_validation=False
        )
        res = create_config.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建飞书配置失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == FEISHU_CONFIG_NAME
        assert "feishu" in data.get("spec", {})

    def test_create_feishu_receiver(self):
        """创建飞书接收方"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/feishu_config", "create_feishu_receiver"
        )
        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="receivers"),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = create_api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建飞书接收方失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == FEISHU_RECEIVER_NAME
        assert "feishu" in data.get("spec", {})
        logger.info(f"飞书接收方创建成功: {FEISHU_RECEIVER_NAME}")


@pytest.mark.notification
class TestVerifyFeishuConfig:
    """验证飞书通知配置"""

    def test_verify_feishu_config(self):
        """验证飞书通知配置"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/feishu_config", "verify_feishu_body"
        )

        api = VerifyAPI_1(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 202), \
            f"验证飞书配置失败，状态码: {res.cached_response.raw_response.status_code}"


@pytest.mark.notification
class TestUpdateFeishuConfig:
    """更新飞书通知渠道 (PUT)"""

    def test_update_feishu_config(self):
        """修改飞书通知配置"""
        if not get_for_test_feishu_config():
            pytest.skip("无法创建飞书配置")

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="configs", name=FEISHU_CONFIG_NAME),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        assert res.cached_response.raw_response.status_code == 200

        current_config = res.cached_response.raw_response.json()

        body = build_update_body(current_config, remove_resource_version=False)
        body.setdefault("metadata", {}).setdefault("annotations", {})["kubesphere.io/alias-name"] = "updated-feishu-config"

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="configs", name=FEISHU_CONFIG_NAME),
            request_body=body,
            enable_schema_validation=False
        )
        update_res = update_api.send()

        assert update_res.cached_response.raw_response.status_code == 200, \
            f"更新飞书配置失败，状态码: {update_res.cached_response.raw_response.status_code}"

        updated_data = update_res.cached_response.raw_response.json()
        annotations = updated_data.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "updated-feishu-config", \
            "注解应已更新"


@pytest.mark.notification
class TestUpdateFeishuReceiver:
    """更新飞书接收方 (PUT)"""

    def test_update_feishu_receiver(self):
        """修改飞书接收方"""
        if not get_for_test_feishu_receiver():
            pytest.skip("无法创建标准飞书接收方")

        # GET 当前接收方数据
        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="receivers", name=FEISHU_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_api.query_params.type = "feishu"
        res = get_api.send()
        assert res.cached_response.raw_response.status_code == 200

        current_receiver = res.cached_response.raw_response.json()

        body = build_update_body(current_receiver, remove_resource_version=False)
        body["spec"]["feishu"]["enabled"] = False

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="receivers", name=FEISHU_RECEIVER_NAME),
            request_body=body,
            enable_schema_validation=False
        )
        update_res = update_api.send()

        assert update_res.cached_response.raw_response.status_code == 200, \
            f"更新飞书接收方失败，状态码: {update_res.cached_response.raw_response.status_code}"

        updated_data = update_res.cached_response.raw_response.json()
        updated_feishu = updated_data.get("spec", {}).get("feishu", {})
        assert updated_feishu.get("enabled") is False, "enabled 应已禁用"
        assert "43gacfe8" in updated_feishu.get("user", []), "user 列表中应包含 43gacfe8"