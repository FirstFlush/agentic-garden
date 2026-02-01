from datetime import datetime, UTC
from pydantic import BaseModel, Field
from .enums import DecisionOutcome


class DecisionSchema(BaseModel):

    outcome: DecisionOutcome
    confidence: float
    policy_version: str
    created: datetime = Field(default_factory=lambda: datetime.now(UTC))
