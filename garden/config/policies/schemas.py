from pydantic import BaseModel, Field


class LightPolicy(BaseModel):
    # behavior
    photoperiod_on_seconds: int
    photoperiod_off_seconds: int

    # interpretation / calibration
    adc_dark: int
    adc_bright: int

    # state detection
    on_threshold: float
    off_threshold: float
    min_samples: int


class SoilMoisturePolicy(BaseModel):
    ...

class ClimatePolicy(BaseModel):
    ...


class PoliciesConfig(BaseModel):
    """
    Root configuration object for all system policies.
    """
    light: LightPolicy