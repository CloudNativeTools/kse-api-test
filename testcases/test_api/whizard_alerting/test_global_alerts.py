# -*- coding:utf-8 -*-
"""
全局告警列表单接口测试
API: HandleListGlobalAlertsAPI
"""
import pytest

from apis.whizard_alerting.Alerting_Management.apis import HandleListGlobalAlertsAPI


@pytest.mark.alerting_management
class TestListGlobalAlerts:
    """查询全局告警列表"""

    def test_list_success(self):
        """正常查询列表"""
        api = HandleListGlobalAlertsAPI()
        api.query_params.page = "1"
        api.query_params.ascending = "false"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

        data = res.cached_response.raw_response.json()
        assert "items" in data
        assert "totalItems" in data

    def test_list_with_state_filter_firing(self):
        """按状态过滤 - firing"""
        api = HandleListGlobalAlertsAPI()
        api.query_params.state = "firing"
        api.query_params.page = "1"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

    def test_list_with_state_filter_pending(self):
        """按状态过滤 - pending"""
        api = HandleListGlobalAlertsAPI()
        api.query_params.state = "pending"
        api.query_params.page = "1"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

    def test_list_with_keyword_filter(self):
        """按关键词过滤"""
        api = HandleListGlobalAlertsAPI()
        api.query_params.keyword = "test"
        api.query_params.page = "1"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200

    def test_list_with_builtin_filter(self):
        """按内置规则组过滤"""
        api = HandleListGlobalAlertsAPI()
        api.query_params.builtin = "false"
        api.query_params.page = "1"

        res = api.send()
        assert res.cached_response.raw_response.status_code == 200
