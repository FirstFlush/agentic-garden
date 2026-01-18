from datetime import datetime
from pydantic import BaseModel
from typing import Any
from ..hardware.enums import SensorType


class RawObservationSchema(BaseModel):

    sensor_id: str
    sensor_type: SensorType
    payload: dict[str, Any]
    created: datetime