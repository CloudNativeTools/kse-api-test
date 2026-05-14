from apis.whizard_telemetry.events_query.apis import QueryEventsAPI
from aomaker.storage import cache
from utils.time_helpers import resolve_time_range


def query_events_statistics(time_range_key: str = "last_1h", cluster: str = "host", **extra_params):
    """
    查询事件统计信息

    Returns:
        AoResponse
    """
    tr = resolve_time_range(time_range_key, component="whizard_telemetry", module="events_query/events")
    api = QueryEventsAPI(enable_schema_validation=False, response=None)
    api.query_params.operation = "statistics"
    api.query_params.start_time = tr["start_time"]
    api.query_params.end_time = tr["end_time"]
    api.query_params.cluster = cluster
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_events_histogram(time_range_key: str = "last_1h", interval: str = "30m", cluster: str = "host", **extra_params):
    """
    查询事件直方图

    Returns:
        AoResponse
    """
    tr = resolve_time_range(time_range_key, component="whizard_telemetry", module="events_query/events")
    api = QueryEventsAPI(enable_schema_validation=False, response=None)
    api.query_params.operation = "histogram"
    api.query_params.start_time = tr["start_time"]
    api.query_params.end_time = tr["end_time"]
    api.query_params.interval = interval
    api.query_params.cluster = cluster
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_events(time_range_key: str = "last_1h", cluster: str = "host", **extra_params):
    """
    查询事件列表

    Returns:
        AoResponse
    """
    tr = resolve_time_range(time_range_key, component="whizard_telemetry", module="events_query/events")
    api = QueryEventsAPI(enable_schema_validation=False, response=None)
    api.query_params.operation = "query"
    api.query_params.start_time = tr["start_time"]
    api.query_params.end_time = tr["end_time"]
    api.query_params.cluster = cluster
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def get_for_test_events():
    """
    确保测试环境有事件数据可查
    由于 Events 是只读查询接口，仅检查环境连通性

    Returns:
        bool: 环境是否可用
    """
    cache_key = "events_env_ready"
    if cache.get(cache_key):
        return True

    try:
        res = query_events_statistics()
        if res.cached_response.raw_response.status_code == 200:
            cache.set(cache_key, True)
            return True
        return False
    except Exception:
        return False