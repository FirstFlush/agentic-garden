from ..common import GardenEnum


class SensorType(GardenEnum):
    CLIMATE = "climate"
    SOIL_MOISTURE = "soil_moisture"
    LIGHT = "light"


class ActuatorType(GardenEnum):
    WATER_PUMP = "water_pump"
    FAN = "fan"
    LIGHT = "light"
