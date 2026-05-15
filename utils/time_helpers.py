import time


def make_timestamp(hours_ago: int = 0) -> str:
    """生成 Unix 时间戳（秒），支持相对偏移"""
    return str(int(time.time()) - hours_ago * 3600)


def resolve_time_range(data_key: str = "last_1h", component: str = None, module: str = None) -> dict:
    """
    从测试数据中解析 start_time/end_time 时间范围（审计/事件/日志风格）

    JSON 数据文件中的 time_ranges 支持 {{timestamp_last_1h}}、{{timestamp_last_3h}}、
    {{timestamp_last_6h}}、{{timestamp}} 占位符。

    Args:
        data_key: 时间范围键名，如 "last_1h", "last_3h", "last_6h"
        component: 组件名称，如 "whizard_telemetry"
        module: 模块路径，如 "auditing_query/auditing"

    Returns:
        {"start_time": str, "end_time": str}
    """
    if component and module:
        from utils.test_data_helper import load_test_data
        raw = load_test_data(component, module, "time_ranges", default={}, replace_vars=False)
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

    return {"start_time": make_timestamp(1), "end_time": make_timestamp(0)}


def resolve_traffic_time_range(hours_ago: int = 1) -> dict:
    """生成简单的 start_time/end_time 时间范围（HTTP 流量日志风格）"""
    return {"start_time": make_timestamp(hours_ago), "end_time": make_timestamp(0)}


