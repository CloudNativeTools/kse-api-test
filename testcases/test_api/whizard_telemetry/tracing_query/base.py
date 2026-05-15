import time

from aomaker.storage import cache

from apis.whizard_telemetry.tracing_query.apis import (
    GetServicesAPI,
    GetTracesAPI,
    GetTagsAPI,
    GetValuesByTagAPI,
    GetServiceGraphAPI,
    GetAssociatedWorkloadAPI,
    GetSpansAPI,
)


def _now() -> int:
    return int(time.time())


def get_services():
    api = GetServicesAPI(enable_schema_validation=False, response=None)
    return api.send()


def build_trace_request_body(start_time: int, end_time: int, **overrides) -> dict:
    body = {
        "startTime": start_time,
        "endTime": end_time,
        "order": "desc",
        "sort": "time",
        "size": 10,
        "from": 0,
        "parameters": [],
    }
    for k, v in overrides.items():
        key = k.rstrip("_")  # from_ -> from
        body[key] = v
    return body


def query_traces(hours_ago: int = 1, **overrides):
    end = _now()
    start = end - hours_ago * 3600
    body = build_trace_request_body(start, end, **overrides)
    api = GetTracesAPI(request_body=body, enable_schema_validation=False, response=None)
    return api.send()


def get_tags():
    api = GetTagsAPI(enable_schema_validation=False, response=None)
    return api.send()


def get_values_by_tag(**extra_params):
    api = GetValuesByTagAPI(enable_schema_validation=False, response=None)
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def query_service_graph(hours_ago: int = 3, **extra_body):
    end = _now()
    start = int(end - hours_ago * 3600)
    body = {"startTime": start, "endTime": end}
    body.update(extra_body)
    api = GetServiceGraphAPI(request_body=body, enable_schema_validation=False, response=None)
    return api.send()


def get_workloads(keys: str = "", hours_ago: int = 3):
    end = _now()
    start = end - hours_ago * 3600
    api = GetAssociatedWorkloadAPI(enable_schema_validation=False, response=None)
    api.query_params.keys = [keys] if keys else []
    api.query_params.startTime = str(start)
    api.query_params.endTime = str(end)
    return api.send()


def query_spans(hours_ago: int = 1, **overrides):
    end = _now()
    start = end - hours_ago * 3600
    body = build_trace_request_body(start, end, **overrides)
    body["sort"] = "duration"
    api = GetSpansAPI(request_body=body, enable_schema_validation=False, response=None)
    return api.send()


def get_for_test_tracing():
    cache_key = "tracing_env_ready"
    if cache.get(cache_key):
        return True
    try:
        res = get_services()
        if res.cached_response.raw_response.status_code == 200:
            cache.set(cache_key, True)
            return True
        return False
    except Exception:
        return False