"""
静默策略(Silence)单接口测试
API: CreateResourceAPI_1, GetResourceAPI_1, PatchResourceAPI_1, UpdateResourceAPI_1, DeleteResourceAPI_1 (resources="silences")

测试策略：
1. 使用固定资源名 silent-autotest-all 贯穿创建、编辑、查询、删除
2. 创建接口在测试类中通过 fixture 清理已有资源，确保幂等
3. PATCH 使用最小请求体只更新特定字段
4. PUT 先 GET 获取当前数据，清理只读字段后修改再提交
5. 静默策略是 Global 级别，不区分多集群
"""
import pytest
from loguru import logger

from apis.whizard_telemetry.notification.apis import (
    GetResourceAPI_1,
    CreateResourceAPI_1,
    PatchResourceAPI_1,
    UpdateResourceAPI_1,
    DeleteResourceAPI_1,
)
from testcases.test_api.whizard_telemetry.notification.base import (
    SILENCE_NAME,
    get_for_test_silence,
    build_update_body,
    delete_resource_if_exists,
)
from utils.api_helpers import deep_merge
from utils.test_data_helper import load_test_data


@pytest.mark.notification
class TestCreateSilence:
    """创建静默策略"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_before_create(self):
        delete_resource_if_exists("silences", SILENCE_NAME)
        yield

    def test_create_silence(self):
        """使用固定名称创建静默策略"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/silence_config", "create_silence"
        )
        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="silences"),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = create_api.send()
        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == SILENCE_NAME
        assert data.get("spec", {}).get("matcher") is not None
        logger.info(f"静默策略创建成功: {SILENCE_NAME}")


@pytest.mark.notification
class TestGetSilence:
    """查看静默策略详情"""

    def test_get_silence(self):
        """正常查看静默策略详情"""
        if not get_for_test_silence():
            pytest.skip("无法创建静默策略")

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            enable_schema_validation=False,
            response=None
        )
        res = get_api.send()
        assert res.cached_response.raw_response.status_code == 200, \
            f"查询失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == SILENCE_NAME
        assert "spec" in data
        logger.info(f"静默策略查询成功: {SILENCE_NAME}")


@pytest.mark.notification
class TestPatchSilenceInfo:
    """编辑静默策略信息（别名和描述）"""

    def test_patch_silence_info(self):
        """PATCH 编辑静默策略的别名和描述"""
        if not get_for_test_silence():
            pytest.skip("无法创建静默策略")

        patch_body = load_test_data(
            "whizard_telemetry", "notification/silence_config", "patch_info"
        )
        patch_api = PatchResourceAPI_1(
            path_params=PatchResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            request_body=patch_body,
            enable_schema_validation=False
        )
        res = patch_api.send()
        assert res.cached_response.raw_response.status_code == 200, \
            f"编辑信息失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        annotations = data.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "alias-test"
        assert annotations.get("kubesphere.io/description") == "desc-test"
        logger.info(f"静默策略信息编辑成功: alias-name=alias-test, description=desc-test")


@pytest.mark.notification
class TestPatchSilenceDuration:
    """编辑静默策略的静默时间"""

    def test_patch_silence_duration(self):
        """PATCH 编辑静默策略的持续时间"""
        if not get_for_test_silence():
            pytest.skip("无法创建静默策略")

        patch_body = load_test_data(
            "whizard_telemetry", "notification/silence_config", "patch_duration"
        )
        patch_api = PatchResourceAPI_1(
            path_params=PatchResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            request_body=patch_body,
            enable_schema_validation=False
        )
        res = patch_api.send()
        assert res.cached_response.raw_response.status_code == 200, \
            f"编辑静默时间失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("spec", {}).get("duration") == "21h52m21s"
        logger.info(f"静默策略持续时间编辑成功: duration=21h52m21s")


@pytest.mark.notification
class TestPatchSilenceMatcher:
    """编辑静默策略的静默条件"""

    def test_patch_silence_matcher(self):
        """PATCH 编辑静默策略的匹配条件"""
        if not get_for_test_silence():
            pytest.skip("无法创建静默策略")

        patch_body = load_test_data(
            "whizard_telemetry", "notification/silence_config", "patch_matcher"
        )
        patch_api = PatchResourceAPI_1(
            path_params=PatchResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            request_body=patch_body,
            enable_schema_validation=False
        )
        res = patch_api.send()
        assert res.cached_response.raw_response.status_code == 200, \
            f"编辑静默条件失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        match_expressions = data.get("spec", {}).get("matcher", {}).get("matchExpressions", [])
        assert len(match_expressions) > 0
        assert match_expressions[0].get("key") == "cluster"
        assert match_expressions[0].get("operator") == "In"
        assert "host" in match_expressions[0].get("values", [])
        logger.info(f"静默策略匹配条件编辑成功: cluster In [host]")


@pytest.mark.notification
class TestUpdateSilenceYaml:
    """编辑静默策略 YAML (PUT)"""

    def test_update_silence_yaml(self):
        """PUT 编辑静默策略完整 YAML"""
        if not get_for_test_silence():
            pytest.skip("无法创建静默策略")

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code == 200

        current_data = get_res.cached_response.raw_response.json()
        body = build_update_body(current_data, remove_resource_version=False)
        patch = load_test_data("whizard_telemetry", "notification/silence_config", "update_silence_yaml")
        body = deep_merge(body, patch)

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            request_body=body,
            enable_schema_validation=False
        )
        update_res = update_api.send()
        assert update_res.cached_response.raw_response.status_code == 200, \
            f"编辑 YAML 失败，状态码: {update_res.cached_response.raw_response.status_code}"

        updated_data = update_res.cached_response.raw_response.json()
        annotations = updated_data.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "alias-test1"
        assert annotations.get("kubesphere.io/description") == "desc-test1"
        logger.info(f"静默策略 YAML 编辑成功: alias-name=alias-test1, description=desc-test1")


@pytest.mark.notification
class TestDeleteSilence:
    """删除静默策略"""

    def test_delete_silence(self):
        """删除静默策略"""
        if not get_for_test_silence():
            pytest.skip("无法创建静默策略")

        delete_api = DeleteResourceAPI_1(
            path_params=DeleteResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            enable_schema_validation=False,
            response=None
        )
        delete_res = delete_api.send()
        assert delete_res.cached_response.raw_response.status_code in (200, 204), \
            f"删除失败，状态码: {delete_res.cached_response.raw_response.status_code}"

        data = delete_res.cached_response.raw_response.json()
        assert data.get("message") == "success"
        logger.info(f"静默策略删除成功: {SILENCE_NAME}")


