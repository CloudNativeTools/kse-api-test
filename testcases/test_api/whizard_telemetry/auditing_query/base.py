import time

from apis.whizard_telemetry.auditing_query.apis import QueryAuditingAPI
from aomaker.storage import cache


def make_timestamp(hours_ago: int = 0) -> str:
    return str(int(time.time()) - hours_ago * 3600)


def resolve_auditing_time_range(data_key: str = "last_1h") -> dict:
    from utils.test_data_helper import load_test_data
    raw = load_test_data("whizard_telemetry", "auditing_query/auditing", "time_ranges", default={}, replace_vars=False)
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


def query_auditing_statistics(time_range_key: str = "last_1h", cluster: str = "host", **extra_params):
    tr = resolve_auditing_time_range(time_range_key)
    api = QueryAuditingAPI(enable_schema_validation=False, response=None)
    api.query_params.operation = "statistics"
    api.query_params.start_time = tr["start_time"]
    api.query_params.end_time = tr["end_time"]
    api.query_params.cluster = cluster
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_auditing_histogram(time_range_key: str = "last_1h", interval: str = "30m", cluster: str = "host", **extra_params):
    tr = resolve_auditing_time_range(time_range_key)
    api = QueryAuditingAPI(enable_schema_validation=False, response=None)
    api.query_params.operation = "histogram"
    api.query_params.start_time = tr["start_time"]
    api.query_params.end_time = tr["end_time"]
    api.query_params.interval = interval
    api.query_params.cluster = cluster
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_auditing(time_range_key: str = "last_1h", cluster: str = "host", **extra_params):
    tr = resolve_auditing_time_range(time_range_key)
    api = QueryAuditingAPI(enable_schema_validation=False, response=None)
    api.query_params.operation = "query"
    api.query_params.start_time = tr["start_time"]
    api.query_params.end_time = tr["end_time"]
    api.query_params.cluster = cluster
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def get_for_test_auditing():
    cache_key = "auditing_env_ready"
    if cache.get(cache_key):
        return True

    try:
        res = query_auditing_statistics()
        if res.cached_response.raw_response.status_code == 200:
            cache.set(cache_key, True)
            return True
        return False
    except Exception:
        return False