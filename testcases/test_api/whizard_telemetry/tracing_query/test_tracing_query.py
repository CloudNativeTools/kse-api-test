import pytest

from utils.api_helpers import get_http_info
from utils.test_data_helper import load_test_data

from testcases.test_api.whizard_telemetry.tracing_query.base import (
    get_services,
    query_traces,
    query_spans,
    get_tags,
    get_values_by_tag,
    query_service_graph,
    get_workloads,
    get_for_test_tracing,
)

QUERY_PARAMS = load_test_data("whizard_telemetry", "tracing_query/data", "query_params", default={})
SERVICE_GRAPH = load_test_data("whizard_telemetry", "tracing_query/data", "service_graph_params", default={})
TAG_VALUES = load_test_data("whizard_telemetry", "tracing_query/data", "tag_value_params", default={})
WORKLOAD_KEYS = load_test_data("whizard_telemetry", "tracing_query/data", "workload_keys", default="")


@pytest.mark.whizard_tracing
class TestGetServices:
    """获取服务列表"""

    def test_services_success(self):
        """获取服务list - 成功"""
        res = get_services()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_tracing
class TestQueryTraces:
    """链路列表查询"""

    def test_traces_default(self):
        """查询10个链路列表 - 默认参数"""
        res = query_traces()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "traces" in data or "total" in data

    def test_traces_by_trace_id(self):
        """按链路ID查询 - 先list取第一条traceId再过滤"""
        list_res = query_traces()
        status, text = get_http_info(list_res)
        assert status == 200, f"list查询失败: {status}, {text}"
        list_data = list_res.cached_response.raw_response.json()
        traces = list_data.get("traces") or []
        assert traces, "链路列表为空，无法获取traceId"
        first_trace_id = traces[0].get("traceId")
        assert first_trace_id, "第一条链路缺少traceId"

        filter_res = query_traces(parameters=[{"field": "traceId", "operator": "?", "values": [first_trace_id]}])
        status, text = get_http_info(filter_res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        filter_data = filter_res.cached_response.raw_response.json()
        filter_traces = filter_data.get("traces") or []
        assert len(filter_traces) >= 1, "按traceId过滤应返回至少1条链路"
        assert filter_traces[0].get("traceId") == first_trace_id, \
            f"traceId不匹配: expected '{first_trace_id}', got '{filter_traces[0].get('traceId')}'"

    def test_traces_by_span_name(self):
        """按span名称查询"""
        span_cfg = QUERY_PARAMS.get("trace_query_by_span_name", {})
        expected_name = span_cfg.get("parameters", [{}])[0].get("values", [""])[0]
        res = query_traces(size=5, **span_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        traces = data.get("traces") or []
        assert len(traces) <= 5, f"expected at most 5 traces, got {len(traces)}"
        for trace in traces:
            spans = trace.get("spans") or []
            assert any(span.get("name") == expected_name for span in spans), \
                f"trace {trace.get('traceId')}: no span matches name '{expected_name}'"

    def test_traces_by_tag(self):
        """按tag查询"""
        tag_cfg = QUERY_PARAMS.get("trace_query_by_tag", {})
        res = query_traces(**tag_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traces_max_duration(self):
        """按最大持续时间查询 - 校验每条trace的spans duration <= 阈值"""
        dur_cfg = QUERY_PARAMS.get("trace_query_max_duration", {})
        max_val = dur_cfg.get("parameters", [{}])[0].get("value")
        res = query_traces(size=5, **dur_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        traces = data.get("traces") or []
        assert len(traces) <= 5
        for trace in traces:
            spans = trace.get("spans") or []
            assert any(span.get("duration", 0) <= max_val for span in spans), \
                f"trace {trace.get('traceId')}: no span duration <= {max_val}"

    def test_traces_min_duration(self):
        """按最小持续时间查询 - 校验每条trace的spans duration >= 阈值"""
        dur_cfg = QUERY_PARAMS.get("trace_query_min_duration", {})
        min_val = dur_cfg.get("parameters", [{}])[0].get("value")
        res = query_traces(size=5, **dur_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        traces = data.get("traces") or []
        assert len(traces) <= 5
        for trace in traces:
            spans = trace.get("spans") or []
            assert any(span.get("duration", 0) >= min_val for span in spans), \
                f"trace {trace.get('traceId')}: no span duration >= {min_val}"

    def test_traces_host_cluster(self):
        """查询host集群链路 - 校验所有spans的cluster=host"""
        host_cfg = QUERY_PARAMS.get("trace_query_host", {})
        expected_cluster = host_cfg.get("parameters", [{}])[0].get("values", [""])[0]
        res = query_traces(**host_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        traces = data.get("traces") or []
        for trace in traces:
            spans = trace.get("spans") or []
            for span in spans:
                assert span.get("cluster") == expected_cluster, \
                    f"trace {trace.get('traceId')} span {span.get('spanId')}: " \
                    f"expected cluster='{expected_cluster}', got '{span.get('cluster')}'"

    def test_traces_ascending_time(self):
        """按起始时间升序"""
        res = query_traces(order="asc", sort="time")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traces_descending_duration(self):
        """按持续时间降序"""
        res = query_traces(order="desc", sort="duration")
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traces_pagination(self):
        """分页查询 - from=1"""
        res = query_traces(from_=1)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"

    def test_traces_recent_2h(self):
        """查询最近2小时"""
        res = query_traces(hours_ago=2)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_tracing
class TestQuerySpans:
    """Span查询"""

    def test_spans_default(self):
        """查询span列表 - 默认参数"""
        res = query_spans()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "spans" in data or "total" in data

    def test_spans_pagination(self):
        """查询span - 分页 size=5"""
        res = query_spans(size=5)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        spans = data.get("spans") or []
        assert len(spans) <= 5


@pytest.mark.whizard_tracing
class TestGetTags:
    """标签查询"""

    def test_tags_success(self):
        """查询tag - 成功"""
        res = get_tags()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_tracing
class TestGetValuesByTag:
    """标签值查询"""

    def test_values_by_tag_success(self):
        """查询tag对应的value - 校验返回包含查询的tag且值非空"""
        params = {k: v for k, v in TAG_VALUES.items() if v}
        expected_tag = params.get("tags", "")
        res = get_values_by_tag(**params)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert expected_tag in data, f"响应缺少tag '{expected_tag}'"
        values = data[expected_tag]
        assert isinstance(values, list) and len(values) > 0, \
            f"tag '{expected_tag}' 的值应为非空列表"


@pytest.mark.whizard_tracing
class TestServiceGraph:
    """服务拓扑查询"""

    def test_service_graph_all(self):
        """获取服务拓扑 - 全部集群"""
        res = query_service_graph()
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert "nodes" in data or "edges" in data

    def test_service_graph_host(self):
        """获取服务拓扑 - host集群, 校验所有nodes的details.cluster=host"""
        host_cfg = SERVICE_GRAPH.get("service_graph_host", {})
        expected_cluster = host_cfg.get("parameters", [{}])[0].get("values", [""])[0]
        res = query_service_graph(**host_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        nodes = data.get("nodes") or []
        for node in nodes:
            assert node.get("details", {}).get("cluster") == expected_cluster, \
                f"node {node.get('id')}: expected cluster='{expected_cluster}', " \
                f"got '{node.get('details', {}).get('cluster')}'"

    def test_service_graph_recent_10m(self):
        """获取服务拓扑 - 最近10分钟"""
        res = query_service_graph(hours_ago=10 / 60)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"


@pytest.mark.whizard_tracing
class TestWorkloads:
    """工作负载查询"""

    def test_workloads_success(self):
        """获取workloads - 校验返回key匹配且workload有name/kind/pods"""
        res = get_workloads(keys=WORKLOAD_KEYS)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        assert WORKLOAD_KEYS in data, f"响应缺少key '{WORKLOAD_KEYS}'"
        workloads = data[WORKLOAD_KEYS]
        assert isinstance(workloads, list) and len(workloads) > 0, "workloads应为非空列表"
        for wl in workloads:
            assert "name" in wl, "workload缺少name"
            assert "kind" in wl, "workload缺少kind"
            pods = wl.get("pods") or []
            assert len(pods) > 0, f"workload {wl.get('name')} 缺少pod"


@pytest.mark.whizard_tracing
@pytest.mark.multi_cluster
class TestTracingMemberCluster:
    """Member集群 - 链路追踪查询"""

    def test_member_traces(self, member_cluster):
        """Member集群 - 查询链路列表, 校验所有spans.cluster=member"""
        member_cfg = QUERY_PARAMS.get("trace_query_member", {})
        res = query_traces(**member_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        traces = data.get("traces") or []
        for trace in traces:
            spans = trace.get("spans") or []
            for span in spans:
                assert span.get("cluster") == member_cluster, \
                    f"trace {trace.get('traceId')} span {span.get('spanId')}: " \
                    f"expected cluster='{member_cluster}', got '{span.get('cluster')}'"

    def test_member_single_service(self, member_cluster):
        """Member集群 - 查询单个服务链路, 校验traces[].services[]存在查询服务"""
        svc_cfg = QUERY_PARAMS.get("trace_query_single_service", {})
        expected_service = svc_cfg.get("parameters", [{}, {}])[1].get("values", [""])[0]
        res = query_traces(**svc_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        traces = data.get("traces") or []
        for trace in traces:
            spans = trace.get("spans") or []
            for span in spans:
                assert span.get("cluster") == member_cluster, \
                    f"trace {trace.get('traceId')} span {span.get('spanId')}: " \
                    f"expected cluster='{member_cluster}', got '{span.get('cluster')}'"
            assert any(expected_service in s for s in (trace.get("services") or [])), \
                f"trace {trace.get('traceId')}: services 中不包含 '{expected_service}'"

    def test_member_service_graph(self, member_cluster):
        """Member集群 - 获取服务拓扑, 校验nodes.details.cluster=member"""
        member_cfg = SERVICE_GRAPH.get("service_graph_member", {})
        res = query_service_graph(**member_cfg)
        status, text = get_http_info(res)
        assert status == 200, f"expected 200, got {status}, body: {text}"
        data = res.cached_response.raw_response.json()
        nodes = data.get("nodes") or []
        for node in nodes:
            assert node.get("details", {}).get("cluster") == member_cluster, \
                f"node {node.get('id')}: expected cluster='{member_cluster}', " \
                f"got '{node.get('details', {}).get('cluster')}'"