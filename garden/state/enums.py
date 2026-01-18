from ..common import GardenEnum


class ClimateTrend(GardenEnum):
    STABLE = "stable"
    DRYING = "drying" 
    HUMIDIFYING = "humidifying"


class LightTrend(GardenEnum):
    INCREASING = "increasing"
    STABLE = "stable"
    DECREASING = "decreasing"

