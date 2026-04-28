from typing import Optional
from attrs import define, field
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "FieldsAPI",
    "LabelvaluesAPI",
    "PlacementAPI",
    "QueryAPI",
    "StatisticsAPI",
    "VerifyAPI",
    "VerifyAPI_1",
]


@define(kw_only=True)
@router.get("/kapis/events.alerting.wiztelemetry.io/v1alpha1/fields")
class FieldsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="fields")


@define(kw_only=True)
@router.get("/kapis/events.alerting.wiztelemetry.io/v1alpha1/labelvalues")
class LabelvaluesAPI(BaseAPI):
    """None"""

    @define
    class QueryParams:
        cluster: Optional[str] = field(default=None)

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="labelvalues")


@define(kw_only=True)
@router.get("/kapis/events.alerting.wiztelemetry.io/v1alpha1/placement")
class PlacementAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="placement")


@define(kw_only=True)
@router.post("/kapis/events.alerting.wiztelemetry.io/v1alpha1/query")
class QueryAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="query")


@define(kw_only=True)
@router.post("/kapis/events.alerting.wiztelemetry.io/v1alpha1/statistics")
class StatisticsAPI(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="statistics")


@define(kw_only=True)
@router.post("/kapis/notification.kubesphere.io/v2beta2/users/{user}/verification")
class VerifyAPI(BaseAPI):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "user name"})

    path_params: PathParams
    endpoint_id: Optional[str] = field(default="Verify")


@define(kw_only=True)
@router.post("/kapis/notification.kubesphere.io/v2beta2/verification")
class VerifyAPI_1(BaseAPI):
    """None"""

    endpoint_id: Optional[str] = field(default="Verify")
