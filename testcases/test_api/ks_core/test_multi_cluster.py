# -*- coding:utf-8 -*-
import pytest

from apis.ks_core.multi_cluster.apis import ListLabelGroupsAPI, CreateLabelsAPI
from apis.ks_core.multi_cluster.models import V1alpha1CreateLabelRequest
from aomaker.storage import cache
from utils.test_data_helper import load_test_data


TEST_LABEL_CONFIG = load_test_data("ks_core", "multi_cluster", "test_labels")
TEST_LABEL_KEY = TEST_LABEL_CONFIG[0].get("key", "test-auto-group") if TEST_LABEL_CONFIG else "test-auto-group"
TEST_LABEL_VALUE = TEST_LABEL_CONFIG[0].get("value", "test-auto-value") if TEST_LABEL_CONFIG else "test-auto-value"


def _ensure_test_label():
    """确保测试标签存在，使用cache缓存避免重复创建"""
    cache_key = f"test_label_{TEST_LABEL_VALUE}"
    
    cached = cache.get(cache_key)
    if cached:
        return True
    
    res = ListLabelGroupsAPI().send()
    data = res.cached_response.raw_response.json()
    
    for items in data.values():
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get("value") == TEST_LABEL_VALUE:
                    cache.set(cache_key, True)
                    return True
    
    create_res = CreateLabelsAPI(request_body=[
        V1alpha1CreateLabelRequest(key=TEST_LABEL_KEY, value=TEST_LABEL_VALUE)
    ]).send()
    
    if create_res.cached_response.raw_response.status_code in (200, 201):
        cache.set(cache_key, True)
        return True
    return False


@pytest.mark.mul_cluster
def test_get_labels_success():
    """获取集群标签列表"""
    if not _ensure_test_label():
        pytest.skip("无法创建测试数据")
    
    res = ListLabelGroupsAPI().send()
    status = res.cached_response.raw_response.status_code
    assert status == 200, f"expected 200, got {status}"
    
    data = res.cached_response.raw_response.json()
    assert isinstance(data, dict) and len(data) > 0
    
    for items in data.values():
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get("value") == TEST_LABEL_VALUE:
                    assert "value" in item and "id" in item
                    return
    
    pytest.fail(f"未找到测试标签: {TEST_LABEL_VALUE}")

