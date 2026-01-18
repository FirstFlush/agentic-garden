from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class SoilMoistureState(BaseModel):
    avg_moisture: float
    trend: float          # slope
    sample_count: int
    confidence: float     # 0–1


class ClimateState(BaseModel):
    created: datetime

    temperature_c: float
    humidity_pct: float

    vpd_kpa: float | None          # derived, optional at first
    trend: Literal["stable", "drying", "humidifying"]

    sample_count: int
    confidence: float              # 0.0 – 1.0


class LightState(BaseModel):
    created: datetime

    intensity: float
    exposure_minutes_today: int

    is_light_on: bool
    trend: Literal["increasing", "stable", "decreasing"]

    sample_count: int
    confidence: float              # 0.0 – 1.0


class DerivedStateSnapshot(BaseModel):
    created: datetime
    soil_moisture: SoilMoistureState | None
    climate: ClimateState | None
    light: LightState | None