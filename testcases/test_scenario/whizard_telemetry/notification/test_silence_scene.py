"""
静默策略场景测试 - 完整工作流
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
    build_update_body,
    delete_resource_if_exists,
)
from utils.api_helpers import deep_merge
from utils.test_data_helper import load_test_data


@pytest.mark.notification
@pytest.mark.scenario
class TestSilenceScenario:
    """静默策略场景测试 - 完整工作流"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_before_scenario(self):
        delete_resource_if_exists("silences", SILENCE_NAME)
        yield

    def test_silence_full_workflow(self):
        """静默策略完整工作流：创建 -> 编辑信息 -> 编辑时间 -> 编辑条件 -> 编辑YAML -> 查看 -> 删除"""
        # 1. 创建静默策略
        create_body = load_test_data(
            "whizard_telemetry", "notification/silence_config", "create_silence"
        )
        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="silences"),
            request_body=create_body,
            enable_schema_validation=False
        )
        create_res = create_api.send()
        assert create_res.cached_response.raw_response.status_code in (200, 201)
        logger.info("1. 静默策略创建成功")

        # 2. 编辑信息（别名和描述）
        patch_info_body = load_test_data(
            "whizard_telemetry", "notification/silence_config", "patch_info"
        )
        patch_info_api = PatchResourceAPI_1(
            path_params=PatchResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            request_body=patch_info_body,
            enable_schema_validation=False
        )
        patch_info_res = patch_info_api.send()
        assert patch_info_res.cached_response.raw_response.status_code == 200
        info_data = patch_info_res.cached_response.raw_response.json()
        annotations = info_data.get("metadata", {}).get("annotations", {})
        assert annotations.get("kubesphere.io/alias-name") == "alias-test"
        assert annotations.get("kubesphere.io/description") == "desc-test"
        logger.info("2. 静默策略信息编辑成功")

        # 3. 编辑静默时间（duration）
        patch_duration_body = load_test_data(
            "whizard_telemetry", "notification/silence_config", "patch_duration"
        )
        patch_duration_api = PatchResourceAPI_1(
            path_params=PatchResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            request_body=patch_duration_body,
            enable_schema_validation=False
        )
        patch_duration_res = patch_duration_api.send()
        assert patch_duration_res.cached_response.raw_response.status_code == 200
        duration_data = patch_duration_res.cached_response.raw_response.json()
        assert duration_data.get("spec", {}).get("duration") == "21h52m21s"
        logger.info("3. 静默时间编辑成功")

        # 4. 编辑静默条件（matcher）
        patch_matcher_body = load_test_data(
            "whizard_telemetry", "notification/silence_config", "patch_matcher"
        )
        patch_matcher_api = PatchResourceAPI_1(
            path_params=PatchResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            request_body=patch_matcher_body,
            enable_schema_validation=False
        )
        patch_matcher_res = patch_matcher_api.send()
        assert patch_matcher_res.cached_response.raw_response.status_code == 200
        matcher_data = patch_matcher_res.cached_response.raw_response.json()
        match_expressions = matcher_data.get("spec", {}).get("matcher", {}).get("matchExpressions", [])
        assert len(match_expressions) == 1
        assert match_expressions[0]["key"] == "cluster"
        assert match_expressions[0]["operator"] == "In"
        assert match_expressions[0]["values"] == ["host"]
        logger.info("4. 静默条件编辑成功")

        # 5. 编辑 YAML (PUT)
        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_res = get_api.send()
        assert get_res.cached_response.raw_response.status_code == 200
        current_data = get_res.cached_response.raw_response.json()
        put_body = build_update_body(current_data, remove_resource_version=False)
        patch = load_test_data("whizard_telemetry", "notification/silence_config", "update_silence_yaml")
        put_body = deep_merge(put_body, patch)

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            request_body=put_body,
            enable_schema_validation=False
        )
        update_res = update_api.send()
        assert update_res.cached_response.raw_response.status_code == 200
        yaml_data = update_res.cached_response.raw_response.json()
        yaml_annotations = yaml_data.get("metadata", {}).get("annotations", {})
        assert yaml_annotations.get("kubesphere.io/alias-name") == "alias-test1"
        assert yaml_annotations.get("kubesphere.io/description") == "desc-test1"
        logger.info("5. 静默策略 YAML 编辑成功")

        # 6. 查看详情 (GET)
        get_api_2 = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_res_2 = get_api_2.send()
        assert get_res_2.cached_response.raw_response.status_code == 200
        detail_data = get_res_2.cached_response.raw_response.json()
        assert detail_data.get("metadata", {}).get("name") == SILENCE_NAME
        logger.info("6. 静默策略查看成功")

        # 7. 删除 (DELETE)
        delete_api = DeleteResourceAPI_1(
            path_params=DeleteResourceAPI_1.PathParams(resources="silences", name=SILENCE_NAME),
            enable_schema_validation=False,
            response=None
        )
        delete_res = delete_api.send()
        assert delete_res.cached_response.raw_response.status_code in (200, 204)
        delete_data = delete_res.cached_response.raw_response.json()
        assert delete_data.get("message") == "success"
        logger.info("7. 静默策略删除成功")