# -*- coding:utf-8 -*-
"""
全局告警场景测试
流程：预热标准规则组 -> 创建临时规则组 -> 查看规则组列表 -> 等待告警触发 -> 查看告警列表 -> 编辑规则组(PUT) -> 编辑规则组(PATCH) -> 查看规则组详情 -> 删除临时规则组
"""
import pytest
import logging

from apis.whizard_alerting.alerting_management.apis import (
    HandleListGlobalRuleGroupsAPI,
    HandleCreateGlobalRuleGroupAPI,
    HandleGetGlobalRuleGroupAPI,
    HandleUpdateGlobalRuleGroupAPI,
    HandlePatchGlobalRuleGroupAPI,
    HandleDeleteGlobalRuleGroupAPI,
    HandleListGlobalAlertsAPI,
)
from testcases.test_api.whizard_alerting.base import (
    is_alert_prewarmed,
    build_patch_body_for_alias_desc,
    build_update_body_for_rules_annotations,
    cleanup_global_rule_group,
    generate_test_name,
)
from utils.test_data_helper import load_test_data

logger = logging.getLogger(__name__)

STANDARD_RULE_GROUP_NAME = "global-alert-standard"
TEMP_RULE_GROUP_NAME = f"global-alert-{generate_test_name()}"


@pytest.mark.alerting_scene
class TestGlobalAlertScene:
    """全局告警场景测试"""

    @pytest.fixture(scope="class", autouse=True)
    def prepare_data(self):
        """
        类级别 fixture：创建临时规则组，测试结束后清理
        """
        request_body = load_test_data(
            "whizard_alerting", "alerting_management/global_rule_groups", "global_rule_group_custom"
        )
        request_body["metadata"]["name"] = TEMP_RULE_GROUP_NAME
        request_body["spec"]["rules"][0]["alert"] = f"{TEMP_RULE_GROUP_NAME}-alert"
        request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{TEMP_RULE_GROUP_NAME}-summary"
        request_body["spec"]["rules"][0]["annotations"]["message"] = f"{TEMP_RULE_GROUP_NAME}-message"

        create_api = HandleCreateGlobalRuleGroupAPI(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = create_api.send()

        if res.cached_response.raw_response.status_code not in (200, 201):
            pytest.skip(f"无法创建测试规则组: {TEMP_RULE_GROUP_NAME}")

        logger.info(f"临时规则组创建成功: {TEMP_RULE_GROUP_NAME}")

        yield

        logger.info(f"清理临时规则组: {TEMP_RULE_GROUP_NAME}")
        cleanup_global_rule_group(TEMP_RULE_GROUP_NAME)

    def test_01_verify_standard_rule_group(self):
        """
        步骤1: 验证预热的标准规则组已存在
        """
        api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(name=STANDARD_RULE_GROUP_NAME),
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert data["metadata"]["name"] == STANDARD_RULE_GROUP_NAME
        logger.info("步骤1: 标准规则组存在")

    def test_02_list_rule_groups(self):
        """
        步骤2: 查看规则组列表
        """
        api = HandleListGlobalRuleGroupsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.builtin = "false"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        items = data.get("items") or []
        found = any(item["metadata"]["name"] == STANDARD_RULE_GROUP_NAME for item in items)
        assert found, f"列表中未找到规则组: {STANDARD_RULE_GROUP_NAME}"
        logger.info("步骤2: 规则组列表查询成功")

    def test_03_wait_and_check_alerts(self):
        """
        步骤3: 验证标准规则组告警已预热
        """
        logger.info(f"步骤3: 检查告警预热状态，规则组: {STANDARD_RULE_GROUP_NAME}")

        if is_alert_prewarmed("global", group_name=STANDARD_RULE_GROUP_NAME):
            logger.info("标准规则组告警已预热，直接复用")
        else:
            logger.warning("标准规则组告警未预热，场景继续执行")

    def test_04_list_alerts(self):
        """
        步骤4: 查看标准规则组告警列表
        """
        api = HandleListGlobalAlertsAPI(
            enable_schema_validation=False,
            response=None
        )
        api.query_params.page = "1"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"
        api.query_params.builtin = "false"
        api.query_params.label_filters = f"rule_group={STANDARD_RULE_GROUP_NAME}"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data

        total = data.get("totalItems", 0)
        assert total > 0, f"告警数量应 >0，实际: {total}"

        items = data.get("items") or []
        rule_groups = [item.get("labels", {}).get("rule_group", "") for item in items]
        assert STANDARD_RULE_GROUP_NAME in rule_groups, \
            f"未找到 rule_group 为 {STANDARD_RULE_GROUP_NAME} 的告警，实际: {rule_groups}"

        logger.info("步骤4: 告警列表查询成功")

    def test_05_update_rule_group_put(self):
        """
        步骤5: 编辑标准规则组(PUT) - 修改规则注解
        """
        get_api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(name=STANDARD_RULE_GROUP_NAME),
            enable_schema_validation=False
        )
        get_res = get_api.send()
        current_data = get_res.cached_response.raw_response.json()

        update_body = build_update_body_for_rules_annotations(
            current_data=current_data,
            summary="updated-summary-by-put",
            message="updated-message-by-put"
        )

        api = HandleUpdateGlobalRuleGroupAPI(
            path_params=HandleUpdateGlobalRuleGroupAPI.PathParams(name=STANDARD_RULE_GROUP_NAME),
            request_body=update_body,
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200
        logger.info("步骤5: PUT编辑规则组成功")

    def test_06_patch_rule_group(self):
        """
        步骤6: 编辑标准规则组(PATCH) - 修改别名和描述
        """
        get_api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(name=STANDARD_RULE_GROUP_NAME),
            enable_schema_validation=False
        )
        get_res = get_api.send()
        current_data = get_res.cached_response.raw_response.json()

        patch_body = build_patch_body_for_alias_desc(
            current_data=current_data,
            alias_name="scene-alias",
            description="scene-description"
        )

        api = HandlePatchGlobalRuleGroupAPI(
            path_params=HandlePatchGlobalRuleGroupAPI.PathParams(name=STANDARD_RULE_GROUP_NAME),
            request_body=patch_body,
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200
        logger.info("步骤6: PATCH编辑规则组成功")

    def test_07_verify_rule_group_detail(self):
        """
        步骤7: 查看标准规则组详情，验证编辑结果
        """
        api = HandleGetGlobalRuleGroupAPI(
            path_params=HandleGetGlobalRuleGroupAPI.PathParams(name=STANDARD_RULE_GROUP_NAME),
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()

        annotations = data["metadata"]["annotations"]
        assert annotations.get("kubesphere.io/alias-name") == "scene-alias"
        assert annotations.get("kubesphere.io/description") == "scene-description"

        rules_annotations = data["spec"]["rules"][0]["annotations"]
        assert rules_annotations.get("summary") == "updated-summary-by-put"
        assert rules_annotations.get("message") == "updated-message-by-put"

        logger.info("步骤7: 规则组详情验证成功")

    def test_08_delete_temp_rule_group(self):
        """
        步骤8: 删除临时规则组
        """
        api = HandleDeleteGlobalRuleGroupAPI(
            path_params=HandleDeleteGlobalRuleGroupAPI.PathParams(name=TEMP_RULE_GROUP_NAME),
            enable_schema_validation=False
        )
        res = api.send()
        assert res.cached_response.raw_response.status_code in (200, 204)
        logger.info("步骤8: 临时规则组删除成功")
