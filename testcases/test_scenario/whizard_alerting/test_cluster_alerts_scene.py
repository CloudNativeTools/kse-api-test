# -*- coding:utf-8 -*-
"""
集群侧告警场景测试
流程：预热标准规则组 -> 创建临时规则组 -> 查看规则组列表 -> 等待告警触发 -> 查看告警列表 -> 编辑规则组(PUT) -> 编辑规则组(PATCH) -> 查看规则组详情 -> 删除临时规则组
"""
import pytest
import logging

from apis.whizard_alerting.alerting_management.apis import (
    HandleListClusterRuleGroupsAPI,
    HandleCreateClusterRuleGroupAPI,
    HandleGetClusterRuleGroupAPI,
    HandleUpdateClusterRuleGroupAPI,
    HandlePatchClusterRuleGroupAPI,
    HandleDeleteClusterRuleGroupAPI,
    HandleListClusterAlertsAPI,
)
from testcases.conftest import host_cluster
from testcases.test_api.whizard_alerting.base import (
    is_alert_prewarmed,
    build_patch_body_for_alias_desc,
    build_update_body_for_rules_annotations,
    cleanup_cluster_rule_group,
    generate_test_name,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

logger = logging.getLogger(__name__)

STANDARD_RULE_GROUP_NAME = "cluster-alert-standard"
TEMP_RULE_GROUP_NAME = f"cluster-alert-{generate_test_name()}"


@pytest.mark.alerting_scene
class TestClusterAlertScene:
    """集群侧告警场景测试"""

    @pytest.fixture(scope="class", autouse=True)
    def prepare_data(self, host_cluster):
        """
        类级别 fixture：创建临时规则组，测试结束后清理
        """
        set_current_cluster(host_cluster)
        try:
            request_body = load_test_data(
                "whizard_alerting", "alerting_management/cluster_rule_groups", "cluster_rule_group_custom"
            )
            request_body["metadata"]["name"] = TEMP_RULE_GROUP_NAME
            request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{TEMP_RULE_GROUP_NAME}-summary"
            request_body["spec"]["rules"][0]["annotations"]["message"] = f"{TEMP_RULE_GROUP_NAME}-message"

            create_api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=host_cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = create_api.send()

            if res.cached_response.raw_response.status_code not in (200, 201):
                pytest.skip(f"无法创建测试规则组: {TEMP_RULE_GROUP_NAME}")

            logger.info(f"临时规则组创建成功: {TEMP_RULE_GROUP_NAME}")
        finally:
            clear_current_cluster()

        yield

        logger.info(f"清理临时规则组: {TEMP_RULE_GROUP_NAME}")
        cleanup_cluster_rule_group(host_cluster, TEMP_RULE_GROUP_NAME)

    def test_01_verify_standard_rule_group(self, host_cluster):
        """
        步骤1: 验证预热的标准规则组已存在
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert data["metadata"]["name"] == STANDARD_RULE_GROUP_NAME
            logger.info("步骤1: 标准规则组存在")
        finally:
            clear_current_cluster()

    def test_02_list_rule_groups(self, host_cluster):
        """
        步骤2: 查看规则组列表
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterRuleGroupsAPI(
                path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=host_cluster)
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
        finally:
            clear_current_cluster()

    def test_03_wait_and_check_alerts(self, host_cluster):
        """
        步骤3: 验证标准规则组告警已预热
        """
        logger.info(f"步骤3: 检查告警预热状态，规则组: {STANDARD_RULE_GROUP_NAME}")

        prewarmed = is_alert_prewarmed("cluster", cluster=host_cluster, group_name=STANDARD_RULE_GROUP_NAME)
        if prewarmed:
            logger.info("标准规则组告警已预热，直接复用")
        else:
            logger.warning("标准规则组告警未预热，场景继续执行")

    def test_04_list_alerts(self, host_cluster):
        """
        步骤4: 查看标准规则组告警列表
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleListClusterAlertsAPI(
                path_params=HandleListClusterAlertsAPI.PathParams(cluster=host_cluster)
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
        finally:
            clear_current_cluster()

    def test_05_update_rule_group_put(self, host_cluster):
        """
        步骤5: 编辑标准规则组(PUT) - 修改规则注解
        """
        set_current_cluster(host_cluster)
        try:
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            get_res = get_api.send()
            current_data = get_res.cached_response.raw_response.json()

            update_body = build_update_body_for_rules_annotations(
                current_data=current_data,
                summary="updated-summary-by-put",
                message="updated-message-by-put"
            )

            api = HandleUpdateClusterRuleGroupAPI(
                path_params=HandleUpdateClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP_NAME
                ),
                request_body=update_body,
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
            logger.info("步骤5: PUT编辑规则组成功")
        finally:
            clear_current_cluster()

    def test_06_patch_rule_group(self, host_cluster):
        """
        步骤6: 编辑标准规则组(PATCH) - 修改别名和描述
        """
        set_current_cluster(host_cluster)
        try:
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            get_res = get_api.send()
            current_data = get_res.cached_response.raw_response.json()

            patch_body = build_patch_body_for_alias_desc(
                current_data=current_data,
                alias_name="scene-alias",
                description="scene-description"
            )

            api = HandlePatchClusterRuleGroupAPI(
                path_params=HandlePatchClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP_NAME
                ),
                request_body=patch_body,
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
            logger.info("步骤6: PATCH编辑规则组成功")
        finally:
            clear_current_cluster()

    def test_07_verify_rule_group_detail(self, host_cluster):
        """
        步骤7: 查看标准规则组详情，验证编辑结果
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=STANDARD_RULE_GROUP_NAME
                ),
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
        finally:
            clear_current_cluster()

    def test_08_delete_temp_rule_group(self, host_cluster):
        """
        步骤8: 删除临时规则组
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleDeleteClusterRuleGroupAPI(
                path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=TEMP_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code in (200, 204)
            logger.info("步骤8: 临时规则组删除成功")
        finally:
            clear_current_cluster()


@pytest.mark.alerting_scene
@pytest.mark.multi_cluster
class TestClusterAlertSceneMember:
    """Member 集群 - 集群侧告警场景测试"""

    MEMBER_STANDARD_RULE_GROUP_NAME = "member-cluster-alert-standard"
    MEMBER_TEMP_RULE_GROUP_NAME = f"member-cluster-alert-{generate_test_name()}"

    @pytest.fixture(scope="class", autouse=True)
    def prepare_data(self, member_cluster):
        """
        类级别 fixture：创建临时规则组，测试结束后清理
        """
        set_current_cluster(member_cluster)
        try:
            request_body = load_test_data(
                "whizard_alerting", "alerting_management/cluster_rule_groups", "cluster_rule_group_custom"
            )
            request_body["metadata"]["name"] = self.MEMBER_TEMP_RULE_GROUP_NAME
            request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{self.MEMBER_TEMP_RULE_GROUP_NAME}-summary"
            request_body["spec"]["rules"][0]["annotations"]["message"] = f"{self.MEMBER_TEMP_RULE_GROUP_NAME}-message"

            create_api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=member_cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = create_api.send()

            if res.cached_response.raw_response.status_code not in (200, 201):
                pytest.skip(f"无法创建测试规则组: {self.MEMBER_TEMP_RULE_GROUP_NAME}")

            logger.info(f"临时规则组创建成功: {self.MEMBER_TEMP_RULE_GROUP_NAME}")
        finally:
            clear_current_cluster()

        yield

        logger.info(f"清理临时规则组: {self.MEMBER_TEMP_RULE_GROUP_NAME}")
        cleanup_cluster_rule_group(member_cluster, self.MEMBER_TEMP_RULE_GROUP_NAME)

    def test_01_verify_standard_rule_group(self, member_cluster):
        """步骤1: 验证预热的标准规则组存在，校验 owner_cluster 标签"""
        set_current_cluster(member_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_STANDARD_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            labels = data["metadata"]["labels"]
            assert labels.get("alerting.kubesphere.io/owner_cluster") == member_cluster
            logger.info("步骤1: Member 集群标准规则组存在")
        finally:
            clear_current_cluster()

    def test_02_list_rule_groups(self, member_cluster):
        """步骤2: 查看规则组列表"""
        set_current_cluster(member_cluster)
        try:
            api = HandleListClusterRuleGroupsAPI(
                path_params=HandleListClusterRuleGroupsAPI.PathParams(cluster=member_cluster)
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.builtin = "false"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            items = data.get("items") or []
            found = any(item["metadata"]["name"] == self.MEMBER_STANDARD_RULE_GROUP_NAME for item in items)
            assert found, f"列表中未找到规则组: {self.MEMBER_STANDARD_RULE_GROUP_NAME}"
            logger.info("步骤2: 规则组列表查询成功")
        finally:
            clear_current_cluster()

    def test_03_wait_and_check_alerts(self, member_cluster):
        """步骤3: 验证标准规则组告警已预热"""
        logger.info(f"步骤3: 检查告警预热状态，规则组: {self.MEMBER_STANDARD_RULE_GROUP_NAME}")

        if is_alert_prewarmed("cluster", cluster=member_cluster, group_name=self.MEMBER_STANDARD_RULE_GROUP_NAME):
            logger.info("标准规则组告警已预热，直接复用")
        else:
            logger.warning("标准规则组告警未预热，场景继续执行")

    def test_04_list_alerts(self, member_cluster):
        """步骤4: 查看标准规则组告警列表"""
        set_current_cluster(member_cluster)
        try:
            api = HandleListClusterAlertsAPI(
                path_params=HandleListClusterAlertsAPI.PathParams(cluster=member_cluster)
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.builtin = "false"
            api.query_params.label_filters = f"rule_group={self.MEMBER_STANDARD_RULE_GROUP_NAME}"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data

            total = data.get("totalItems", 0)
            assert total > 0, f"告警数量应 >0，实际: {total}"

            items = data.get("items") or []
            rule_groups = [item.get("labels", {}).get("rule_group", "") for item in items]
            assert self.MEMBER_STANDARD_RULE_GROUP_NAME in rule_groups, \
                f"未找到 rule_group 为 {self.MEMBER_STANDARD_RULE_GROUP_NAME} 的告警，实际: {rule_groups}"

            logger.info("步骤4: 告警列表查询成功")
        finally:
            clear_current_cluster()

    def test_05_update_rule_group_put(self, member_cluster):
        """步骤5: PUT编辑标准规则组"""
        set_current_cluster(member_cluster)
        try:
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_STANDARD_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            get_res = get_api.send()
            current_data = get_res.cached_response.raw_response.json()

            update_body = build_update_body_for_rules_annotations(
                current_data=current_data,
                summary="member-updated-summary",
                message="member-updated-message"
            )

            api = HandleUpdateClusterRuleGroupAPI(
                path_params=HandleUpdateClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_STANDARD_RULE_GROUP_NAME
                ),
                request_body=update_body,
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
            logger.info("步骤5: PUT编辑规则组成功")
        finally:
            clear_current_cluster()

    def test_06_patch_rule_group(self, member_cluster):
        """步骤6: PATCH编辑标准规则组"""
        set_current_cluster(member_cluster)
        try:
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_STANDARD_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            get_res = get_api.send()
            current_data = get_res.cached_response.raw_response.json()

            patch_body = build_patch_body_for_alias_desc(
                current_data=current_data,
                alias_name="member-scene-alias",
                description="member-scene-description"
            )

            api = HandlePatchClusterRuleGroupAPI(
                path_params=HandlePatchClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_STANDARD_RULE_GROUP_NAME
                ),
                request_body=patch_body,
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200
            logger.info("步骤6: PATCH编辑规则组成功")
        finally:
            clear_current_cluster()

    def test_07_verify_rule_group_detail(self, member_cluster):
        """步骤7: 查看标准规则组详情，验证编辑结果"""
        set_current_cluster(member_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_STANDARD_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            annotations = data["metadata"]["annotations"]
            assert annotations.get("kubesphere.io/alias-name") == "member-scene-alias"
            assert annotations.get("kubesphere.io/description") == "member-scene-description"

            rules_annotations = data["spec"]["rules"][0]["annotations"]
            assert rules_annotations.get("summary") == "member-updated-summary"
            logger.info("步骤7: 规则组详情验证成功")
        finally:
            clear_current_cluster()

    def test_08_delete_temp_rule_group(self, member_cluster):
        """步骤8: 删除临时规则组"""
        set_current_cluster(member_cluster)
        try:
            api = HandleDeleteClusterRuleGroupAPI(
                path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_TEMP_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code in (200, 204)
            logger.info("步骤8: 临时规则组删除成功")
        finally:
            clear_current_cluster()
