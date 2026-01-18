import logging
from .base import BaseStateService
from ..schemas import LightState
from ...hardware.schemas import LightPayload
from ..dto import ParsedObservation
from ...storage.schemas import RawObservationSchema

logger = logging.getLogger(__name__)


class LightStateService(BaseStateService[LightPayload, LightState]):

    _payload_schema = LightPayload
    _state_schema = LightState

    def _derive_state(self, observations: list[ParsedObservation[LightPayload]]) -> LightState:
        is_light_on = self._is_light_on(observations[-1])


    def _is_light_on(self, observation: ParsedObservation[LightPayload]) -> bool:
        ...