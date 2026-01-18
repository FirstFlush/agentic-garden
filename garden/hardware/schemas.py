from pydantic import BaseModel


class SensorPayload(BaseModel):
    pass


class ClimatePayload(SensorPayload):
    temp: float         # Celsius
    humidity: float     # Relative Humidity


class LightPayload(SensorPayload):
    # read actual sesnor output
    ...

class SoilMoisturePayload(SensorPayload):
    # read actual sensor output
    ...