from ..common import GardenEnum


class SensorType(GardenEnum):
    DHT22 = "dht22"
    EK1940 = "ek1940"
    PHOTO_RESISTOR = "photo_resistor"


class ActuatorType(GardenEnum):
    WATER_PUMP = "water_pump"
    FAN = "fan"
    GROW_LIGHT = "grow_light"
