from datetime import datetime, UTC
from pydantic import BaseModel, Field
from ..action.enums import ActionType


class LLMResponse(BaseModel):
    """Response from the LLM service."""

    action: ActionType
    raw_response: dict = Field(default_factory=dict)
    model: str
    created: datetime = Field(default_factory=lambda: datetime.now(UTC))
