"""
通知语言单接口测试
API: GetResourceAPI_1, PatchResourceAPI_1 (resources="notificationmanagers", name="notification-manager")

测试策略：
1. GET 查询当前通知语言
2. PATCH 切换语言为 zh-cn 并验证
3. PATCH 恢复原始语言（fixture teardown）
"""
import pytest
from loguru import logger

from apis.whizard_telemetry.notification.apis import (
    GetResourceAPI_1,
    PatchResourceAPI_1,
)

NOTIFICATION_MANAGER = "notification-manager"


def get_notification_manager():
    api = GetResourceAPI_1(
        path_params=GetResourceAPI_1.PathParams(
            resources="notificationmanagers",
            name=NOTIFICATION_MANAGER,
        ),
        enable_schema_validation=False,
        response=None,
    )
    return api.send()


def patch_notification_manager(body: dict):
    api = PatchResourceAPI_1(
        path_params=PatchResourceAPI_1.PathParams(
            resources="notificationmanagers",
            name=NOTIFICATION_MANAGER,
        ),
        request_body=body,
        enable_schema_validation=False,
        response=None,
    )
    return api.send()


@pytest.mark.notification
class TestGetNotificationLanguage:
    """查询通知语言"""

    def test_get_language_success(self):
        """查询通知语言 - 成功"""
        res = get_notification_manager()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "spec" in data
        assert "template" in data["spec"]
        assert "language" in data["spec"]["template"]

        logger.info(f"当前通知语言: {data['spec']['template']['language']}")


@pytest.mark.notification
class TestPatchNotificationLanguage:
    """切换通知语言（自动恢复原始语言）"""

    @pytest.fixture(scope="class", autouse=True)
    def record_and_restore_language(self):
        res = get_notification_manager()
        assert res.cached_response.raw_response.status_code == 200
        original = res.cached_response.raw_response.json()["spec"]["template"]["language"]
        logger.info(f"原始通知语言: {original}")

        yield

        patch_body = {"spec": {"template": {"language": original}}}
        restore_res = patch_notification_manager(patch_body)
        assert restore_res.cached_response.raw_response.status_code == 200
        logger.info(f"通知语言已恢复为 {original}")

    def test_patch_language_to_chinese(self):
        """切换通知语言为中文 (zh-cn) 并验证"""
        patch_body = {"spec": {"template": {"language": "zh-cn"}}}
        res = patch_notification_manager(patch_body)
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert data["spec"]["template"]["language"] == "zh-cn"
        logger.info("通知语言已切换为 zh-cn，验证通过")

        get_res = get_notification_manager()
        assert get_res.cached_response.raw_response.status_code == 200
        assert get_res.cached_response.raw_response.json()["spec"]["template"]["language"] == "zh-cn"
        logger.info("语言切换已持久化")