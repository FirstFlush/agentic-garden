from datetime import datetime
from pydantic import BaseModel
from typing import Any
from .enums import SensorType


class SensorReadingSchema(BaseModel):

    sensor_id: str
    sensor_type: SensorType
    payload: dict[str, Any]
    created: datetime


class SensorPayload(BaseModel):
    pass


class ClimatePayload(SensorPayload):
    temp: float         # Celsius
    humidity: float     # Relative Humidity


class LightPayload(SensorPayload):
    # read actual sesnor output
    raw_adc: int    


class SoilMoisturePayload(SensorPayload):
    # read actual sensor output
    raw_adc: int