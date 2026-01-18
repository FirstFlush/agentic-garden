from pydantic import BaseModel


class SensorPayload(BaseModel):
    pass


class ClimatePayload(SensorPayload):
    temp: float         # Celsius
    humidity: float     # Relative Humidity


class LightPayload(SensorPayload):
    # read actual sesnor output
    raw_adc: int    


class SoilMoisturePayload(SensorPayload):
    # read actual sensor output
    raw_adc: int