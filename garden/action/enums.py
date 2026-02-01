from ..common.enums import GardenEnum


class ActionType(GardenEnum):
    LIGHT_ON = "light_on"
    LIGHT_OFF = "light_off"
    WATER_SMALL = "water_small"
    WATER_MEDIUM = "water_medium"
    WATER_LARGE = "water_large"
    FAN_ON = "fan_on"
    FAN_OFF = "fan_off"
    NO_ACTION = "no_action"
    ALL_STOP = "all_stop"


class ActionResult(GardenEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"