"""
Webhook通知渠道单接口测试
API: ListResourceAPI_1, CreateResourceAPI_1, UpdateResourceAPI_1, VerifyAPI_1

测试策略：
1. 使用标准资源 global-webhook-receiver / global-webhook-config-secret 贯穿查询、修改接口
2. get_for_test 确保资源存在（查不到就创建）
3. 创建接口单独测试（创建新资源）
4. Webhook 没有 config 资源，仅有 secret 和 receiver
5. 前置条件：确保 webhook 基础设施（TLS Secret、ConfigMap、Deployment、Service）存在
6. 通知渠道是 Global 级别，不区分多集群
"""
import pytest
import time
from loguru import logger

from apis.whizard_telemetry.notification.apis import (
    ListResourceAPI_1,
    GetResourceAPI_1,
    CreateResourceAPI_1,
    UpdateResourceAPI_1,
    VerifyAPI_1,
)
from testcases.test_api.whizard_telemetry.notification.base import (
    WEBHOOK_RECEIVER_NAME,
    WEBHOOK_SECRET_NAME,
    get_for_test_webhook_secret,
    get_for_test_webhook_receiver,
    build_update_body,
    delete_resource_if_exists,
)
from utils.test_data_helper import load_test_data
from utils.cluster_helpers import set_current_cluster, clear_current_cluster, get_clusters
from apis.ks_core.namespaced_resources.apis import (
    CreateNamespacedDeploymentAPI,
    GetNamespacedDeploymentAPI,
    ListNamespacedResourcesAPI,
    CreateNamespacedSecretAPI,
    CreateNamespacedConfigMapAPI,
    CreateNamespacedServiceAPI,
)


# ============ Webhook 前置条件：基础设施准备 ============

WEBHOOK_NAMESPACE = "default"
WEBHOOK_TLS_SECRET = "webhook-tls"
WEBHOOK_CONFIGMAP = "nginx-config"
WEBHOOK_DEPLOYMENT = "webhook-service"
WEBHOOK_SERVICE = "webhook-service"


def _ensure_resource_exists(cluster: str, resource_type: str, resource_name: str,
                             test_data_key: str, create_api_cls) -> bool:
    set_current_cluster(cluster)
    try:
        list_api = ListNamespacedResourcesAPI(
            path_params=ListNamespacedResourcesAPI.PathParams(
                namespace=WEBHOOK_NAMESPACE, resources=resource_type,
            ),
            query_params=ListNamespacedResourcesAPI.QueryParams(
                name=resource_name, limit="10", page="1", sortBy="updateTime",
            ),
            enable_schema_validation=False, response=None,
        )
        res = list_api.send()
        if res.cached_response.raw_response.status_code == 200:
            items = res.cached_response.raw_response.json().get("items", [])
            if any(item.get("metadata", {}).get("name") == resource_name for item in items):
                return True

        body = load_test_data("whizard_telemetry", "notification/webhook_config", test_data_key)
        create_api = create_api_cls(
            path_params=create_api_cls.PathParams(namespace=WEBHOOK_NAMESPACE),
            request_body=body, enable_schema_validation=False,
        )
        create_res = create_api.send()
        return create_res.cached_response.raw_response.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"确保 {resource_type}/{resource_name} 失败: {e}")
        return False
    finally:
        clear_current_cluster()


def _ensure_tls_secret(cluster: str) -> bool:
    return _ensure_resource_exists(cluster, "secrets", WEBHOOK_TLS_SECRET,
                                    "create_webhook_tls_secret", CreateNamespacedSecretAPI)


def _ensure_configmap(cluster: str) -> bool:
    return _ensure_resource_exists(cluster, "configmaps", WEBHOOK_CONFIGMAP,
                                    "create_webhook_configmap", CreateNamespacedConfigMapAPI)


def _ensure_deployment(cluster: str) -> bool:
    set_current_cluster(cluster)
    try:
        list_api = ListNamespacedResourcesAPI(
            path_params=ListNamespacedResourcesAPI.PathParams(
                namespace=WEBHOOK_NAMESPACE, resources="deployments",
            ),
            query_params=ListNamespacedResourcesAPI.QueryParams(
                name=WEBHOOK_DEPLOYMENT, limit="10", page="1", sortBy="updateTime",
            ),
            enable_schema_validation=False, response=None,
        )
        res = list_api.send()
        exists = False
        if res.cached_response.raw_response.status_code == 200:
            items = res.cached_response.raw_response.json().get("items", [])
            exists = any(item.get("metadata", {}).get("name") == WEBHOOK_DEPLOYMENT for item in items)

        if not exists:
            body = load_test_data("whizard_telemetry", "notification/webhook_config", "create_webhook_deployment")
            create_api = CreateNamespacedDeploymentAPI(
                path_params=CreateNamespacedDeploymentAPI.PathParams(namespace=WEBHOOK_NAMESPACE),
                request_body=body, enable_schema_validation=False,
            )
            create_res = create_api.send()
            if create_res.cached_response.raw_response.status_code not in (200, 201):
                return False
            logger.info("Deployment 已创建，等待就绪...")
        else:
            logger.info("Deployment 已存在，检查是否就绪...")

        max_retries = 30
        for attempt in range(max_retries):
            get_api = GetNamespacedDeploymentAPI(
                path_params=GetNamespacedDeploymentAPI.PathParams(
                    namespace=WEBHOOK_NAMESPACE, name=WEBHOOK_DEPLOYMENT,
                ),
                enable_schema_validation=False, response=None,
            )
            get_res = get_api.send()
            if get_res.cached_response.raw_response.status_code != 200:
                time.sleep(5)
                continue

            status = get_res.cached_response.raw_response.json().get("status", {})
            ready = status.get("readyReplicas", 0)
            available = status.get("availableReplicas", 0)
            if ready >= 1 and available >= 1:
                logger.info(f"Deployment 就绪 (readyReplicas={ready}, availableReplicas={available})")
                return True

            logger.info(f"等待 Deployment 就绪... ({attempt+1}/{max_retries}) readyReplicas={ready}")
            time.sleep(5)

        logger.warning("Deployment 超时未就绪")
        return False
    except Exception as e:
        logger.warning(f"确保 Deployment 失败: {e}")
        return False
    finally:
        clear_current_cluster()


def _ensure_service(cluster: str) -> bool:
    return _ensure_resource_exists(cluster, "services", WEBHOOK_SERVICE,
                                    "create_webhook_service", CreateNamespacedServiceAPI)


def setup_webhook_infrastructure() -> bool:
    host_cluster, _ = get_clusters()
    if not host_cluster:
        logger.warning("无法获取 host 集群")
        return False

    steps = [
        ("TLS secret", _ensure_tls_secret),
        ("ConfigMap", _ensure_configmap),
        ("Deployment", _ensure_deployment),
        ("Service", _ensure_service),
    ]

    for name, fn in steps:
        if not fn(host_cluster):
            logger.warning(f"Webhook 基础设施 {name} 检查/创建失败")
            return False
        logger.info(f"Webhook 基础设施 {name} 就绪")

    return True


# ============ 测试用例 ============

@pytest.fixture(scope="module", autouse=True)
def ensure_webhook_infrastructure():
    if not setup_webhook_infrastructure():
        pytest.skip("Webhook 基础设施准备失败，跳过所有测试")


@pytest.mark.notification
class TestListWebhookSecret:
    """查询webhook secret"""

    def test_list_secrets_success(self):
        """按名称过滤 - 查询webhook secret"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="secrets"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.name = WEBHOOK_SECRET_NAME
        api.query_params.type = "webhook"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        found = any(
            item.get("metadata", {}).get("name") == WEBHOOK_SECRET_NAME
            for item in (data.get("items") or [])
        )
        assert found, f"webhook secret {WEBHOOK_SECRET_NAME} 应存在于列表中"


@pytest.mark.notification
class TestListWebhookReceiver:
    """查询webhook接收方"""

    def test_list_receivers_with_type_filter(self):
        """按类型过滤 - 查询webhook接收方"""
        api = ListResourceAPI_1(
            path_params=ListResourceAPI_1.PathParams(resources="receivers"),
            enable_schema_validation=False,
            response=None
        )
        api.query_params.type = "webhook"
        api.query_params.limit = "10"
        api.query_params.sortBy = "createTime"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data
        items = data.get("items") or []
        for item in items:
            assert "webhook" in item.get("spec", {}), f"非webhook接收方: {item.get('metadata', {}).get('name')}"


@pytest.mark.notification
class TestCreateWebhookConfig:
    """创建webhook通知渠道"""

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_before_create(self):
        delete_resource_if_exists("receivers", WEBHOOK_RECEIVER_NAME)
        delete_resource_if_exists("secrets", WEBHOOK_SECRET_NAME)
        yield

    def test_create_webhook_secret(self):
        """创建webhook secret"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/webhook_config", "create_webhook_secret"
        )
        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="secrets"),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = create_api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建webhook secret失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == WEBHOOK_SECRET_NAME
        logger.info(f"webhook secret创建成功: {WEBHOOK_SECRET_NAME}")

    def test_create_webhook_receiver(self):
        """创建webhook接收方"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/webhook_config", "create_webhook_receiver"
        )
        create_api = CreateResourceAPI_1(
            path_params=CreateResourceAPI_1.PathParams(resources="receivers"),
            request_body=request_body,
            enable_schema_validation=False
        )
        res = create_api.send()

        assert res.cached_response.raw_response.status_code in (200, 201), \
            f"创建webhook接收方失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("metadata", {}).get("name") == WEBHOOK_RECEIVER_NAME
        assert "webhook" in data.get("spec", {})
        logger.info(f"webhook接收方创建成功: {WEBHOOK_RECEIVER_NAME}")


@pytest.mark.notification
class TestVerifyWebhookConfig:
    """验证webhook通知配置"""

    def test_verify_webhook(self):
        """验证webhook通知配置"""
        request_body = load_test_data(
            "whizard_telemetry", "notification/webhook_config", "verify_webhook_body"
        )

        api = VerifyAPI_1(
            request_body=request_body,
            enable_schema_validation=False
        )
        res = api.send()

        assert res.cached_response.raw_response.status_code in (200, 202), \
            f"验证webhook配置失败，状态码: {res.cached_response.raw_response.status_code}"

        data = res.cached_response.raw_response.json()
        assert data.get("Status") == 200
        assert "successfully" in data.get("Message", "").lower()


@pytest.mark.notification
class TestUpdateWebhookReceiver:
    """更新webhook接收方 (PUT)"""

    def test_update_webhook_receiver(self):
        """修改webhook接收方"""
        if not get_for_test_webhook_receiver():
            pytest.skip("无法创建标准webhook接收方")

        get_api = GetResourceAPI_1(
            path_params=GetResourceAPI_1.PathParams(resources="receivers", name=WEBHOOK_RECEIVER_NAME),
            enable_schema_validation=False,
            response=None
        )
        get_api.query_params.type = "webhook"
        res = get_api.send()
        assert res.cached_response.raw_response.status_code == 200

        current_receiver = res.cached_response.raw_response.json()

        body = build_update_body(current_receiver, remove_resource_version=False)
        body["spec"]["webhook"]["enabled"] = False

        update_api = UpdateResourceAPI_1(
            path_params=UpdateResourceAPI_1.PathParams(resources="receivers", name=WEBHOOK_RECEIVER_NAME),
            request_body=body,
            enable_schema_validation=False
        )
        update_res = update_api.send()

        assert update_res.cached_response.raw_response.status_code == 200, \
            f"更新webhook接收方失败，状态码: {update_res.cached_response.raw_response.status_code}"

        updated_data = update_res.cached_response.raw_response.json()
        updated_webhook = updated_data.get("spec", {}).get("webhook", {})
        assert updated_webhook.get("enabled") is False, "enabled 应已禁用"
        assert "url" in updated_webhook