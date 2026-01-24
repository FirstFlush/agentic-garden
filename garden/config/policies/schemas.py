from pydantic import BaseModel, Field, model_validator


class LightAdcCalibration(BaseModel):
    dark: int = Field(..., ge=0)
    bright: int = Field(..., ge=0)

    @model_validator(mode="after")
    def check_range(self):
        if self.dark >= self.bright:
            raise ValueError("adc.dark must be < adc.bright")
        return self


class LightOnOffInterpretation(BaseModel):
    on_threshold: float = Field(..., gt=0.0, lt=1.0)
    off_threshold: float = Field(..., gt=0.0, lt=1.0)
    min_samples: int = Field(..., ge=1)

    @model_validator(mode="after")
    def check_hysteresis(self):
        if self.off_threshold >= self.on_threshold:
            raise ValueError("off_threshold must be < on_threshold")
        return self


class LightInterpretation(BaseModel):
    on_off: LightOnOffInterpretation


class LightPhotoperiod(BaseModel):
    on_seconds: int = Field(..., gt=0)
    off_seconds: int = Field(..., gt=0)


class LightSchedule(BaseModel):
    photoperiod: LightPhotoperiod


class LightCalibration(BaseModel):
    adc: LightAdcCalibration


class LightPolicy(BaseModel):
    calibration: LightCalibration
    interpretation: LightInterpretation
    schedule: LightSchedule


class SoilAdcCalibration(BaseModel):
    dry: int = Field(..., ge=0)
    wet: int = Field(..., ge=0)

    @model_validator(mode="after")
    def check_range(self):
        if self.wet >= self.dry:
            raise ValueError("adc.wet must be < adc.dry")
        return self


class SoilLevelInterpretation(BaseModel):
    dry_threshold: float = Field(..., gt=0.0, lt=1.0)
    wet_threshold: float = Field(..., gt=0.0, lt=1.0)
    min_samples: int = Field(..., ge=1)

    @model_validator(mode="after")
    def check_thresholds(self):
        if self.wet_threshold >= self.dry_threshold:
            raise ValueError("wet_threshold must be < dry_threshold")
        return self


class SoilTrendInterpretation(BaseModel):
    lookback_samples: int = Field(..., ge=2)
    min_delta: float = Field(..., gt=0.0)


class SoilMoistureInterpretation(BaseModel):
    level: SoilLevelInterpretation
    trend: SoilTrendInterpretation


class SoilWateringPolicy(BaseModel):
    target_moisture: float = Field(..., gt=0.0, lt=1.0)
    min_interval_seconds: int = Field(..., ge=0)
    max_water_per_event_ml: int = Field(..., gt=0)


class SoilCalibration(BaseModel):
    adc: SoilAdcCalibration


class SoilMoistureIntervention(BaseModel):
    watering: SoilWateringPolicy


class SoilMoisturePolicy(BaseModel):
    calibration: SoilCalibration
    interpretation: SoilMoistureInterpretation
    intervention: SoilMoistureIntervention


class TemperatureAcceptableRange(BaseModel):
    min_c: float
    max_c: float

    @model_validator(mode="after")
    def check_range(self):
        if self.min_c >= self.max_c:
            raise ValueError("min_c must be < max_c")
        return self


class HumidityAcceptableRange(BaseModel):
    min_percent: float
    max_percent: float

    @model_validator(mode="after")
    def check_range(self):
        if self.min_percent >= self.max_percent:
            raise ValueError("min_percent must be < max_percent")
        return self


class ClimateHysteresis(BaseModel):
    min_samples: int = Field(..., ge=1)


class TemperatureInterpretation(BaseModel):
    acceptable: TemperatureAcceptableRange
    hysteresis: ClimateHysteresis


class HumidityInterpretation(BaseModel):
    acceptable: HumidityAcceptableRange
    hysteresis: ClimateHysteresis


class ClimateTrendMinDelta(BaseModel):
    temperature_c: float = Field(..., gt=0.0)
    humidity_percent: float = Field(..., gt=0.0)


class ClimateTrends(BaseModel):
    lookback_seconds: int = Field(..., ge=60)
    min_delta: ClimateTrendMinDelta


class ClimateInterpretation(BaseModel):
    temperature: TemperatureInterpretation
    humidity: HumidityInterpretation
    trends: ClimateTrends


class ClimatePolicy(BaseModel):
    interpretation: ClimateInterpretation


class PoliciesConfig(BaseModel):
    light: LightPolicy
    climate: ClimatePolicy
    soil_moisture: SoilMoisturePolicy