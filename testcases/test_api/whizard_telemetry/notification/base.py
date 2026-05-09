"""
notification 单接口测试基类
提供 get_for_test 函数和公共工具
"""
import time
from loguru import logger

from apis.whizard_telemetry.notification.apis import (
    ListResourceAPI_1,
    GetResourceAPI_1,
    CreateResourceAPI_1,
    UpdateResourceAPI_1,
    DeleteResourceAPI_1,
    VerifyAPI_1,
)
from utils.api_helpers import clean_api_response
from utils.test_data_helper import load_test_data

EMAIL_CONFIG_NAME = "default-email-config"
FEISHU_CONFIG_NAME = "default-feishu-config"
FEISHU_RECEIVER_NAME = "global-feishu-receiver"
EMAIL_SECRET_NAME = "global-email-config-secret"
FEISHU_SECRET_NAME = "global-feishu-config-secret"


def build_update_body(current_data: dict, remove_resource_version: bool = True) -> dict:
    """
    构建通知资源的 PUT/PATCH 请求体，清理只读系统字段。

    Args:
        current_data: GET/LIST 接口返回的完整资源数据
        remove_resource_version: 是否移除 resourceVersion

    Returns:
        清理后的请求体 dict
    """
    return clean_api_response(current_data, remove_resource_version=remove_resource_version)


def _ensure_secret_exists(secret_name: str, module: str, test_data_key: str) -> bool:
    try:
        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="secrets", name=secret_name),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        if res.cached_response.raw_response.status_code == 200:
            return True

        request_body = load_test_data(
            "whizard_telemetry", module, test_data_key
        )
        if not isinstance(request_body, dict):
            return False

        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="secrets"),
            request_body=request_body,
            enable_schema_validation=False
        )
        create_res = create_api.send()
        return create_res.cached_response.raw_response.status_code in (200, 201)

    except Exception as e:
        logger.warning(f"_ensure_secret_exists failed for {secret_name}: {e}")
        return False


def delete_resource_if_exists(resources: str, name: str) -> None:
    """如果资源存在则删除，忽略 404"""
    try:
        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources=resources, name=name),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        if res.cached_response.raw_response.status_code != 200:
            return

        delete_api = DeleteResourceAPI_1(
            path_params=DeleteResourceAPI_1.PathParams(resources=resources, name=name),
            enable_schema_validation=False,
            response=None
        )
        del_res = delete_api.send()
        if del_res.cached_response.raw_response.status_code in (200, 204):
            logger.info(f"已删除现有资源: {resources}/{name}")
    except Exception as e:
        logger.warning(f"_delete_resource_if_exists failed for {resources}/{name}: {e}")


def get_for_test_email_config() -> bool:
    """
    确保 email 配置存在
    1. 先查询，如果已存在，直接返回 True
    2. 如果不存在，调用创建 API 创建
    """
    try:
        if not _ensure_secret_exists(EMAIL_SECRET_NAME, "notification/email_config", "create_email_secret"):
            return False

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="configs", name=EMAIL_CONFIG_NAME),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        if res.cached_response.raw_response.status_code == 200:
            return True

        request_body = load_test_data(
            "whizard_telemetry", "notification/email_config", "create_email_config"
        )
        if not isinstance(request_body, dict):
            return False

        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="configs"),
            request_body=request_body,
            enable_schema_validation=False
        )
        create_res = create_api.send()
        if create_res.cached_response.raw_response.status_code in (200, 201):
            return True
        return False

    except Exception as e:
        logger.warning(f"get_for_test_email_config failed: {e}")
        return False


def get_for_test_feishu_config() -> bool:
    """
    确保 feishu 配置存在
    """
    try:
        if not _ensure_secret_exists(FEISHU_SECRET_NAME, "notification/feishu_config", "create_feishu_secret"):
            return False

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="configs", name=FEISHU_CONFIG_NAME),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        if res.cached_response.raw_response.status_code == 200:
            return True

        request_body = load_test_data(
            "whizard_telemetry", "notification/feishu_config", "create_feishu_config"
        )
        if not isinstance(request_body, dict):
            return False

        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="configs"),
            request_body=request_body,
            enable_schema_validation=False
        )
        create_res = create_api.send()
        if create_res.cached_response.raw_response.status_code in (200, 201):
            return True
        return False

    except Exception as e:
        logger.warning(f"get_for_test_feishu_config failed: {e}")
        return False


def get_for_test_feishu_receiver() -> bool:
    """
    确保 feishu 接收方存在
    """
    try:
        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="receivers", name=FEISHU_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_api.query_params.type = "feishu"
        res = get_api.send()
        if res.cached_response.raw_response.status_code == 200:
            return True

        request_body = load_test_data(
            "whizard_telemetry", "notification/feishu_config", "create_feishu_receiver"
        )
        if not isinstance(request_body, dict):
            return False

        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="receivers"),
            request_body=request_body,
            enable_schema_validation=False
        )
        create_res = create_api.send()
        if create_res.cached_response.raw_response.status_code in (200, 201):
            return True
        return False

    except Exception as e:
        logger.warning(f"get_for_test_feishu_receiver failed: {e}")
        return False


def generate_test_name(prefix: str = "test") -> str:
    """生成测试资源名称"""
    return f"{prefix}-{int(time.time())}"