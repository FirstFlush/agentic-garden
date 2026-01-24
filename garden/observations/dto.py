from dataclasses import dataclass
from datetime import datetime
from ..hardware.schemas import LightPayload, ClimatePayload, SoilMoisturePayload, SensorPayload
from ..hardware.enums import SensorType


@dataclass(frozen=True)
class ParsedObservation:
    created: datetime
    sensor_type: SensorType
    sensor_id: str
    payload: SensorPayload


@dataclass(frozen=True)
class ClimateObservation(ParsedObservation):
    payload: ClimatePayload


@dataclass(frozen=True)
class LightObservation(ParsedObservation):
    payload: LightPayload


@dataclass(frozen=True)
class SoilMoistureObservation(ParsedObservation):
    payload: SoilMoisturePayload