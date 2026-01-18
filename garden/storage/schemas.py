from datetime import datetime
from pydantic import BaseModel
from typing import Any
from ..hardware.enums import SensorType


class RawObservation(BaseModel):

    sensor: SensorType
    payload: dict[str, Any]
    created: datetime