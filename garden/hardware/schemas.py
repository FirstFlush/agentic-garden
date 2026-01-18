from pydantic import BaseModel


class SensorPayload(BaseModel):
    pass


class DHT22Payload(SensorPayload):
    temp: float         # Celsius
    humidity: float     # Relative Humidity