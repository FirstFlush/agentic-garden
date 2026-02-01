from ..common import GardenEnum


class DecisionOutcome(GardenEnum):
    NO_ACTION = "no_action"
    ESCALATE = "escalate"
    ALERT = "alert"
