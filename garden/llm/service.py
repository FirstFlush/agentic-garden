"""
LLM Service for the garden agent.

Calls Claude API with the current state and available tools.
Returns a structured response indicating which action to take.
"""

import logging
import os

from anthropic import Anthropic

from .exc import LLMRequestError, LLMResponseError
from .prompts import PromptBuilder
from .schemas import LLMResponse
from .tools import TOOLS, TOOL_TO_ACTION
from ..action.enums import ActionType
from ..state.schemas import DerivedStateSnapshot

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-4-20250514"


class LLMService:
    """
    Calls Claude to decide what action to take given a state snapshot.

    Responsibilities:
    - Build prompt from state
    - Call Claude API with tools
    - Parse response into LLMResponse

    Does NOT:
    - Execute actions
    - Persist anything
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        prompt_builder: PromptBuilder | None = None,
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise LLMRequestError("ANTHROPIC_API_KEY not set")

        self.model = model
        self.client = Anthropic(api_key=self.api_key)
        self.prompt_builder = prompt_builder or PromptBuilder()

    def request(self, snapshot: DerivedStateSnapshot) -> LLMResponse:
        """
        Send the state snapshot to Claude and get an action decision.

        Args:
            snapshot: The current derived state.

        Returns:
            LLMResponse with the action to take.

        Raises:
            LLMRequestError: If the API call fails.
            LLMResponseError: If the response is invalid.
        """
        system_prompt = self.prompt_builder.system_prompt
        user_message = self.prompt_builder.build_user_message(snapshot)

        logger.debug(f"Sending request to {self.model}")
        logger.debug(f"User message:\n{user_message}")

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=256,
                system=system_prompt,
                tools=TOOLS,
                tool_choice={"type": "any"},
                messages=[
                    {"role": "user", "content": user_message}
                ],
            )
        except Exception as e:
            msg = f"Claude API request failed: {e}"
            logger.error(msg, exc_info=True)
            raise LLMRequestError(msg) from e

        return self._parse_response(response)

    def _parse_response(self, response) -> LLMResponse:
        """Extract the tool call from Claude's response."""
        # Find tool_use block
        tool_use = None
        for block in response.content:
            if block.type == "tool_use":
                tool_use = block
                break

        if tool_use is None:
            msg = f"No tool_use block in response: {response.content}"
            logger.error(msg)
            raise LLMResponseError(msg)

        tool_name = tool_use.name

        if tool_name not in TOOL_TO_ACTION:
            msg = f"Unknown tool: {tool_name}"
            logger.error(msg)
            raise LLMResponseError(msg)

        action_value = TOOL_TO_ACTION[tool_name]
        action = ActionType(action_value)

        return LLMResponse(
            action=action,
            raw_response={
                "id": response.id,
                "tool_name": tool_name,
                "tool_input": tool_use.input,
                "stop_reason": response.stop_reason,
            },
            model=response.model,
        )
