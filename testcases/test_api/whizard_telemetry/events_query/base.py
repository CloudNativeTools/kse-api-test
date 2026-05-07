import time

from apis.whizard_telemetry.events_query.apis import QueryEventsAPI
from aomaker.storage import cache


def make_timestamp(hours_ago: int = 0) -> str:
    """生成 Unix 时间戳（秒），支持相对偏移"""
    return str(int(time.time()) - hours_ago * 3600)


def resolve_event_time_range(data_key: str = "last_1h") -> dict:
    """
    从测试数据中解析时间范围，替换动态时间戳

    Args:
        data_key: 时间范围键名，如 "last_1h", "last_3h", "last_6h"

    Returns:
        {"start_time": str, "end_time": str}
    """
    from utils.test_data_helper import load_test_data
    raw = load_test_data("whizard_telemetry", "events_query/events", "time_ranges", default={}, replace_vars=False)
    tr = raw.get(data_key, {})
    if not tr:
        return {"start_time": make_timestamp(1), "end_time": make_timestamp(0)}

    start_raw = tr.get("start_time", "")
    end_raw = tr.get("end_time", "")

    if "{{timestamp_last_1h}}" in start_raw:
        start = make_timestamp(1)
    elif "{{timestamp_last_3h}}" in start_raw:
        start = make_timestamp(3)
    elif "{{timestamp_last_6h}}" in start_raw:
        start = make_timestamp(6)
    else:
        start = start_raw

    if "{{timestamp}}" in end_raw:
        end = make_timestamp(0)
    else:
        end = end_raw

    return {"start_time": start, "end_time": end}


def query_events_statistics(time_range_key: str = "last_1h", cluster: str = "host", **extra_params):
    """
    查询事件统计信息

    Returns:
        AoResponse
    """
    tr = resolve_event_time_range(time_range_key)
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
    tr = resolve_event_time_range(time_range_key)
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
    tr = resolve_event_time_range(time_range_key)
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