from ..common.exc import GardenException


class LLMServiceException(GardenException):
    """Base exception for LLM service errors."""
    pass


class LLMRequestError(LLMServiceException):
    """Failed to make request to LLM API."""
    pass


class LLMResponseError(LLMServiceException):
    """LLM returned an invalid or unexpected response."""
    pass


class PromptBuildError(LLMServiceException):
    """Failed to build prompt."""
    pass
