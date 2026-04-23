# -*- coding:utf-8 -*-
"""
集群侧告警场景测试
流程：创建规则组 -> 查看规则组列表 -> 等待告警触发 -> 查看告警列表 -> 编辑规则组(PUT) -> 编辑规则组(PATCH) -> 查看规则组详情 -> 删除规则组
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
    wait_for_alerts,
    build_patch_body_for_alias_desc,
    build_update_body_for_rules_annotations,
    cleanup_cluster_rule_group,
    query_cluster_alerts,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

logger = logging.getLogger(__name__)

SCENE_RULE_GROUP_NAME = "scene-cluster-alert"


@pytest.mark.alerting_scene
class TestClusterAlertScene:
    """集群侧告警场景测试"""

    @pytest.fixture(scope="class", autouse=True)
    def prepare_data(self, host_cluster):
        """
        类级别 fixture：创建规则组，测试结束后清理
        """
        set_current_cluster(host_cluster)
        try:
            request_body = load_test_data(
                "whizard_alerting", "alerting_management/cluster_rule_groups", "cluster_rule_group_custom"
            )
            request_body["metadata"]["name"] = SCENE_RULE_GROUP_NAME
            request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{SCENE_RULE_GROUP_NAME}-summary"
            request_body["spec"]["rules"][0]["annotations"]["message"] = f"{SCENE_RULE_GROUP_NAME}-message"

            create_api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=host_cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = create_api.send()

            if res.cached_response.raw_response.status_code not in (200, 201):
                pytest.skip(f"无法创建测试规则组: {SCENE_RULE_GROUP_NAME}")

            logger.info(f"场景规则组创建成功: {SCENE_RULE_GROUP_NAME}")
        finally:
            clear_current_cluster()

        yield

        logger.info(f"清理场景规则组: {SCENE_RULE_GROUP_NAME}")
        cleanup_cluster_rule_group(host_cluster, SCENE_RULE_GROUP_NAME)

    def test_01_create_rule_group(self, host_cluster):
        """
        步骤1: 验证规则组已创建
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=SCENE_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert data["metadata"]["name"] == SCENE_RULE_GROUP_NAME
            logger.info("步骤1: 规则组创建成功")
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
            found = any(item["metadata"]["name"] == SCENE_RULE_GROUP_NAME for item in items)
            assert found, f"列表中未找到规则组: {SCENE_RULE_GROUP_NAME}"
            logger.info("步骤2: 规则组列表查询成功")
        finally:
            clear_current_cluster()

    def test_03_wait_and_check_alerts(self, host_cluster):
        """
        步骤3: 等待告警触发
        """
        logger.info(f"步骤3: 等待告警触发，规则组: {SCENE_RULE_GROUP_NAME}")

        found_alert, _ = wait_for_alerts(
            query_func=lambda: query_cluster_alerts(
                cluster=host_cluster,
                rule_group_name=SCENE_RULE_GROUP_NAME
            ),
            max_attempts=48,
            sleep_interval=5
        )

        if not found_alert:
            logger.warning("告警未触发，场景继续执行")

    def test_04_list_alerts(self, host_cluster):
        """
        步骤4: 查看告警列表
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
            api.query_params.label_filters = f"rule_group={SCENE_RULE_GROUP_NAME}"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data

            total = data.get("totalItems", 0)
            assert total > 0, f"告警数量应 >0，实际: {total}"

            items = data.get("items") or []
            rule_groups = [item.get("labels", {}).get("rule_group", "") for item in items]
            assert SCENE_RULE_GROUP_NAME in rule_groups, \
                f"未找到 rule_group 为 {SCENE_RULE_GROUP_NAME} 的告警，实际: {rule_groups}"

            logger.info("步骤4: 告警列表查询成功")
        finally:
            clear_current_cluster()

    def test_05_update_rule_group_put(self, host_cluster):
        """
        步骤5: 编辑规则组(PUT) - 修改规则注解
        """
        set_current_cluster(host_cluster)
        try:
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=SCENE_RULE_GROUP_NAME
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
                    name=SCENE_RULE_GROUP_NAME
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
        步骤6: 编辑规则组(PATCH) - 修改别名和描述
        """
        set_current_cluster(host_cluster)
        try:
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=SCENE_RULE_GROUP_NAME
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
                    name=SCENE_RULE_GROUP_NAME
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
        步骤7: 查看规则组详情，验证编辑结果
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=SCENE_RULE_GROUP_NAME
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

    def test_08_delete_rule_group(self, host_cluster):
        """
        步骤8: 删除规则组
        """
        set_current_cluster(host_cluster)
        try:
            api = HandleDeleteClusterRuleGroupAPI(
                path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                    cluster=host_cluster,
                    name=SCENE_RULE_GROUP_NAME
                )
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code in (200, 204)
            logger.info("步骤8: 规则组删除成功")
        finally:
            clear_current_cluster()


@pytest.mark.alerting_scene
@pytest.mark.multi_cluster
class TestClusterAlertSceneMember:
    """Member 集群 - 集群侧告警场景测试"""

    MEMBER_RULE_GROUP_NAME = "scene-member-cluster-alert"

    @pytest.fixture(scope="class", autouse=True)
    def prepare_data(self, member_cluster):
        """
        类级别 fixture：创建规则组，测试结束后清理
        """
        set_current_cluster(member_cluster)
        try:
            request_body = load_test_data(
                "whizard_alerting", "alerting_management/cluster_rule_groups", "cluster_rule_group_custom"
            )
            request_body["metadata"]["name"] = self.MEMBER_RULE_GROUP_NAME
            request_body["spec"]["rules"][0]["annotations"]["summary"] = f"{self.MEMBER_RULE_GROUP_NAME}-summary"
            request_body["spec"]["rules"][0]["annotations"]["message"] = f"{self.MEMBER_RULE_GROUP_NAME}-message"

            create_api = HandleCreateClusterRuleGroupAPI(
                path_params=HandleCreateClusterRuleGroupAPI.PathParams(cluster=member_cluster),
                request_body=request_body,
                enable_schema_validation=False
            )
            res = create_api.send()

            if res.cached_response.raw_response.status_code not in (200, 201):
                pytest.skip(f"无法创建测试规则组: {self.MEMBER_RULE_GROUP_NAME}")

            logger.info(f"场景规则组创建成功: {self.MEMBER_RULE_GROUP_NAME}")
        finally:
            clear_current_cluster()

        yield

        logger.info(f"清理场景规则组: {self.MEMBER_RULE_GROUP_NAME}")
        cleanup_cluster_rule_group(member_cluster, self.MEMBER_RULE_GROUP_NAME)

    def test_01_create_and_verify_on_member(self, member_cluster):
        """步骤1: 验证规则组已创建，校验 owner_cluster 标签"""
        set_current_cluster(member_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_RULE_GROUP_NAME
                ),
                enable_schema_validation=False
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            labels = data["metadata"]["labels"]
            assert labels.get("alerting.kubesphere.io/owner_cluster") == member_cluster
            logger.info("步骤1: Member 集群规则组创建成功")
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
            found = any(item["metadata"]["name"] == self.MEMBER_RULE_GROUP_NAME for item in items)
            assert found, f"列表中未找到规则组: {self.MEMBER_RULE_GROUP_NAME}"
            logger.info("步骤2: 规则组列表查询成功")
        finally:
            clear_current_cluster()

    def test_03_wait_and_check_alerts(self, member_cluster):
        """步骤3: 等待告警触发"""
        logger.info(f"步骤3: 等待告警触发，规则组: {self.MEMBER_RULE_GROUP_NAME}")

        def validate_cluster_label(items):
            for item in items:
                cluster_label = item.get("labels", {}).get("cluster")
                assert cluster_label == member_cluster, \
                    f"告警 cluster 标签不匹配: {cluster_label} != {member_cluster}"

        found_alert, _ = wait_for_alerts(
            query_func=lambda: query_cluster_alerts(
                cluster=member_cluster,
                rule_group_name=self.MEMBER_RULE_GROUP_NAME
            ),
            max_attempts=48,
            sleep_interval=5,
            validate_func=validate_cluster_label
        )

        if not found_alert:
            logger.warning("告警未触发，场景继续执行")

    def test_04_list_alerts(self, member_cluster):
        """步骤4: 查看告警列表"""
        set_current_cluster(member_cluster)
        try:
            api = HandleListClusterAlertsAPI(
                path_params=HandleListClusterAlertsAPI.PathParams(cluster=member_cluster)
            )
            api.query_params.page = "1"
            api.query_params.limit = "10"
            api.query_params.builtin = "false"
            api.query_params.label_filters = f"rule_group={self.MEMBER_RULE_GROUP_NAME}"

            res = api.send()
            assert res.cached_response.raw_response.status_code == 200

            data = res.cached_response.raw_response.json()
            assert "items" in data

            total = data.get("totalItems", 0)
            assert total > 0, f"告警数量应 >0，实际: {total}"

            items = data.get("items") or []
            rule_groups = [item.get("labels", {}).get("rule_group", "") for item in items]
            assert self.MEMBER_RULE_GROUP_NAME in rule_groups, \
                f"未找到 rule_group 为 {self.MEMBER_RULE_GROUP_NAME} 的告警，实际: {rule_groups}"

            logger.info("步骤4: 告警列表查询成功")
        finally:
            clear_current_cluster()

    def test_05_update_rule_group_put(self, member_cluster):
        """步骤5: PUT编辑规则组"""
        set_current_cluster(member_cluster)
        try:
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_RULE_GROUP_NAME
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
                    name=self.MEMBER_RULE_GROUP_NAME
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
        """步骤6: PATCH编辑规则组"""
        set_current_cluster(member_cluster)
        try:
            get_api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_RULE_GROUP_NAME
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
                    name=self.MEMBER_RULE_GROUP_NAME
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
        """步骤7: 查看规则组详情，验证编辑结果"""
        set_current_cluster(member_cluster)
        try:
            api = HandleGetClusterRuleGroupAPI(
                path_params=HandleGetClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_RULE_GROUP_NAME
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

    def test_08_delete_rule_group(self, member_cluster):
        """步骤8: 删除规则组"""
        set_current_cluster(member_cluster)
        try:
            api = HandleDeleteClusterRuleGroupAPI(
                path_params=HandleDeleteClusterRuleGroupAPI.PathParams(
                    cluster=member_cluster,
                    name=self.MEMBER_RULE_GROUP_NAME
                )
            )
            res = api.send()
            assert res.cached_response.raw_response.status_code in (200, 204)
            logger.info("步骤8: 规则组删除成功")
        finally:
            clear_current_cluster()
