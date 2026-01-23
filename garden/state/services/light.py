import logging
from .base import BaseStateService
from ..models import LightState
from ..schemas import LightStateSchema
from ...hardware.schemas import LightPayload
from ...observations.dto import ParsedObservation
from ...observations.schemas import RawObservationSchema

logger = logging.getLogger(__name__)


class LightStateService(BaseStateService[LightPayload, LightStateSchema]):

    _payload_schema = LightPayload
    _state_schema = LightState

    def _derive_state(self, observations: list[ParsedObservation[LightPayload]]) -> LightStateSchema:
        is_light_on = self._is_light_on(observations[-1])
        ...

    def _save_state(self, state_schema: LightStateSchema) -> LightState:
        ...


    def _is_light_on(self, observation: ParsedObservation[LightPayload]) -> bool:
        ...