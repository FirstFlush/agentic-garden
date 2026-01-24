from datetime import datetime
from pydantic import BaseModel
from .enums import (
    HumidityLevel,
    HumidityTrend,
    SoilMoistureLevel, 
    SoilMoistureTrend,
    TemperatureLevel,
    TemperatureTrend
)


class DerivedStateSchema(BaseModel):
    window_start: datetime
    window_end: datetime
    sample_count: int
    confidence: float


class SoilMoistureStateSchema(DerivedStateSchema):
    avg_moisture: float              # normalized 0–1
    level: SoilMoistureLevel
    trend: SoilMoistureTrend


class ClimateStateSchema(DerivedStateSchema):
    temperature_c: float
    humidity_rh: float
    vpd_kpa: float | None
    temperature_level: TemperatureLevel
    temperature_trend: TemperatureTrend
    humidity_level: HumidityLevel
    humidity_trend: HumidityTrend


class LightStateSchema(DerivedStateSchema):
    intensity: float
    duration_seconds: int
    is_light_on: bool


class DerivedStateSnapshot(BaseModel):
    created: datetime
    soil_moisture: SoilMoistureStateSchema | None
    climate: ClimateStateSchema | None
    light: LightStateSchema | None