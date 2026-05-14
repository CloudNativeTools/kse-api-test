from apis.whizard_telemetry.auditing_query.apis import QueryAuditingAPI
from aomaker.storage import cache
from utils.time_helpers import resolve_time_range


def query_auditing_statistics(time_range_key: str = "last_1h", cluster: str = "host", **extra_params):
    tr = resolve_time_range(time_range_key, component="whizard_telemetry", module="auditing_query/auditing")
    api = QueryAuditingAPI(enable_schema_validation=False, response=None)
    api.query_params.operation = "statistics"
    api.query_params.start_time = tr["start_time"]
    api.query_params.end_time = tr["end_time"]
    api.query_params.cluster = cluster
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_auditing_histogram(time_range_key: str = "last_1h", interval: str = "30m", cluster: str = "host", **extra_params):
    tr = resolve_time_range(time_range_key, component="whizard_telemetry", module="auditing_query/auditing")
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
    tr = resolve_time_range(time_range_key, component="whizard_telemetry", module="auditing_query/auditing")
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