import time

from apis.whizard_telemetry.notification_query.apis import SearchNotificationAPI
from aomaker.storage import cache


def make_timestamp(seconds_ago: int = 0) -> str:
    return str(int(time.time()) - seconds_ago)


def search_notifications(cluster: str = "host", **extra_params):
    api = SearchNotificationAPI(enable_schema_validation=False, response=None)
    api.query_params.cluster = cluster
    api.query_params.size = 10
    api.query_params.from_ = 0
    for k, v in extra_params.items():
        setattr(api.query_params, k, v)
    return api.send()


def get_for_test_notification_history():
    cache_key = "notification_history_env_ready"
    if cache.get(cache_key):
        return True

    try:
        res = search_notifications()
        if res.cached_response.raw_response.status_code == 200:
            cache.set(cache_key, True)
            return True
        return False
    except Exception:
        return False