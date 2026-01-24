from ..common.enums import GardenEnum


class ActionRequestType(GardenEnum):
    LLM = "llm"
    MANUAL = "manual"
    RULESET = "ruleset"


class ActionResult(GardenEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"