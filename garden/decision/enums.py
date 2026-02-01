from ..common import GardenEnum


class DecisionOutcome(GardenEnum):
    NO_ACTION = "no_action"
    LOCAL_ACTION = "local_action"
    ESCALATE = "escalate"


class EscalationTarget(GardenEnum):
    LLM = "llm"
    ALERT = "alert"