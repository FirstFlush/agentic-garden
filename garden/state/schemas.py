from datetime import datetime
from pydantic import BaseModel
from .enums import LightTrend, ClimateTrend


class DerivedState(BaseModel):
    window_start: datetime
    window_end: datetime
    sample_count: int
    confidence: float


class SoilMoistureState(DerivedState):
    avg_moisture: float
    trend: float


class ClimateState(DerivedState):
    temperature_c: float
    humidity_rh: float
    vpd_kpa: float | None   # derived, optional at first
    trend: ClimateTrend


class LightState(DerivedState):
    intensity: float
    duration_seconds: int
    is_light_on: bool
    # trend: LightTrend     # currently not needed. Will add this if I want the system to be able to adjust lights up/down


class DerivedStateSnapshot(BaseModel):
    created: datetime
    soil_moisture: SoilMoistureState | None
    climate: ClimateState | None
    light: LightState | None