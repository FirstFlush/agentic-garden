from dataclasses import dataclass
from datetime import datetime
from .schemas import LightPayload, ClimatePayload, SoilMoisturePayload, SensorPayload
from .enums import SensorType


@dataclass(frozen=True)
class ParsedSensorReading:
    created: datetime
    sensor_type: SensorType
    sensor_id: str
    payload: SensorPayload


@dataclass(frozen=True)
class ClimateReading(ParsedSensorReading):
    payload: ClimatePayload


@dataclass(frozen=True)
class LightReading(ParsedSensorReading):
    payload: LightPayload


@dataclass(frozen=True)
class SoilMoistureReading(ParsedSensorReading):
    payload: SoilMoisturePayload