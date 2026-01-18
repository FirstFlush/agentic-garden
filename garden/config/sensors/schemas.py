# config/models.py
from pydantic import BaseModel
from typing import List, Optional


class SensorRef(BaseModel):
    id: str
    model: Optional[str] = None
    # Hardware model identifier (driver/ingestion concern only)


class SensorDomainConfig(BaseModel):
    sensors: List[SensorRef]
    window_seconds: int
    sampling_interval_seconds: Optional[int]
    # None means "not polled" / actuator-driven


class SensorsConfig(BaseModel):
    climate: SensorDomainConfig
    soil_moisture: SensorDomainConfig
    light: SensorDomainConfig
