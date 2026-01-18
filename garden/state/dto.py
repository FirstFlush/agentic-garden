from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar
from ..hardware.schemas import SensorPayload
from ..hardware.enums import SensorType

P = TypeVar("P", bound=SensorPayload)


@dataclass(frozen=True)
class ParsedObservation(Generic[P]):
    created: datetime
    sensor_type: SensorType
    sensor_id: str
    payload: P