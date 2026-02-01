from ..common import GardenEnum


class TemperatureLevel(GardenEnum):
    TOO_COLD = "too_cold"
    OK = "ok"
    TOO_HOT = "too_hot"


class TemperatureTrend(GardenEnum):
    COOLING = "cooling"
    STABLE = "stable"
    HEATING = "heating"


class HumidityLevel(GardenEnum):
    TOO_DRY = "too_dry"
    OK = "ok"
    TOO_HUMID = "too_humid"


class HumidityTrend(GardenEnum):
    DRYING = "drying"
    STABLE = "stable"
    HUMIDIFYING = "humidifying"


class SoilMoistureLevel(GardenEnum):
    DRY = "dry"
    OK = "ok"
    WET = "wet"


class SoilMoistureTrend(GardenEnum):
    DRYING = "drying"
    STABLE = "stable"
    WETTING = "wetting"