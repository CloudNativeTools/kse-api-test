import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.tracing_query.base import (
    get_services,
    query_traces,
    get_tags,
    get_values_by_tag,
    query_service_graph,
    get_workloads,
    get_for_test_tracing,
)

QUERY_PARAMS = load_test_data("whizard_telemetry", "tracing_query/data", "query_params", default={})
TAG_VALUES = load_test_data("whizard_telemetry", "tracing_query/data", "tag_value_params", default={})
WORKLOAD_KEYS = load_test_data("whizard_telemetry", "tracing_query/data", "workload_keys", default="")


@pytest.mark.whizard_tracing_scene
class TestTracingAnalysisWorkflow:
    """
    链路追踪分析工作流场景测试
    1. 获取服务列表 -> 2. 查询链路列表 -> 3. 查询标签 -> 4. 按标签查询链路 -> 5. 查询服务拓扑 -> 6. 查询workloads
    """

    @pytest.fixture(scope="class", autouse=True)
    def check_env(self):
        if not get_for_test_tracing():
            pytest.skip("链路追踪查询环境不可用")

    def test_01_get_services(self):
        """步骤1: 获取服务列表"""
        res = get_services()
        status, text = get_http_info(res)
        assert status == 200, f"获取服务列表失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert isinstance(data, list), "服务列表应为数组"
        self.services = data

    def test_02_query_traces(self):
        """步骤2: 查询链路列表"""
        res = query_traces()
        status, text = get_http_info(res)
        assert status == 200, f"查询链路列表失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "traces" in data or "total" in data, "响应中缺少 traces 或 total 字段"

    def test_03_get_tags(self):
        """步骤3: 查询标签"""
        res = get_tags()
        status, text = get_http_info(res)
        assert status == 200, f"查询标签失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert isinstance(data.get("resource"), list), "标签列表应为数组"

    def test_04_query_traces_by_tag(self):
        """步骤4: 按标签查询链路"""
        tag_cfg = QUERY_PARAMS.get("trace_query_by_tag", {})
        res = query_traces(**tag_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"按标签查询链路失败: {status}, {text}"

    def test_05_query_service_graph(self):
        """步骤5: 查询服务拓扑"""
        res = query_service_graph()
        status, text = get_http_info(res)
        assert status == 200, f"查询服务拓扑失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        assert "nodes" in data or "edges" in data, "响应中缺少 nodes 或 edges 字段"

    def test_06_get_workloads(self):
        """步骤6: 查询workloads"""
        res = get_workloads(keys=WORKLOAD_KEYS)
        status, text = get_http_info(res)
        assert status == 200, f"查询workloads失败: {status}, {text}"
        data = res.cached_response.raw_response.json()
        workloads = data[WORKLOAD_KEYS]
        assert isinstance(workloads, list) and len(workloads) > 0, "workloads应为非空列表"

    def test_07_query_traces_host(self):
        """步骤7: 按host集群过滤查询链路"""
        host_cfg = QUERY_PARAMS.get("trace_query_host", {})
        res = query_traces(**host_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"host集群查询链路失败: {status}, {text}"

    def test_08_query_traces_ascending(self):
        """步骤8: 按起始时间升序查询链路"""
        res = query_traces(order="asc", sort="time")
        status, text = get_http_info(res)
        assert status == 200, f"升序查询链路失败: {status}, {text}"

    def test_09_query_traces_desc_duration(self):
        """步骤9: 按持续时间降序查询链路"""
        res = query_traces(order="desc", sort="duration")
        status, text = get_http_info(res)
        assert status == 200, f"持续时间降序查询链路失败: {status}, {text}"

    def test_10_query_service_graph_host(self):
        """步骤10: 查询host集群服务拓扑"""
        host_cfg = {"parameters": [{"field": "cluster", "operator": "=", "values": ["host"]}]}
        res = query_service_graph(**host_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"host集群服务拓扑查询失败: {status}, {text}"