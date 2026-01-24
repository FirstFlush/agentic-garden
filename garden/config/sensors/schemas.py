# config/models.py
from pydantic import BaseModel


class SensorRef(BaseModel):
    id: str
    model: str | None = None    # Hardware model identifier (driver/ingestion concern only)


class SamplingConfig(BaseModel):
    interval_seconds: int


class EvaluationConfig(BaseModel):
    interval_seconds: int


class EvidenceConfig(BaseModel):
    lookback_seconds: int | None = None
    lookback_samples: int | None = None

    def validate_mode(self) -> None:
        if self.lookback_seconds is None and self.lookback_samples is None:
            raise ValueError("Evidence must define either lookback_seconds or lookback_samples")

        if self.lookback_seconds is not None and self.lookback_samples is not None:
            raise ValueError("Evidence cannot define both lookback_seconds and lookback_samples")


class SensorDomainConfig(BaseModel):
    sensors: list[SensorRef]
    sampling: SamplingConfig
    evaluation: EvaluationConfig
    evidence: EvidenceConfig


class SensorsConfig(BaseModel):
    climate: SensorDomainConfig
    soil_moisture: SensorDomainConfig
    light: SensorDomainConfig