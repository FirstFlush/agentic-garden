import datetime
import logging
from .base import BaseStateService
from ..models import LightState
from ..schemas import LightStateSchema
from ...hardware.schemas import LightPayload
from ...observations.dto import LightObservation
from ...observations.schemas import RawObservationSchema


logger = logging.getLogger(__name__)


class LightStateService(BaseStateService):

    def derive_state(self, observations: list[LightObservation]) -> LightStateSchema:
        intensity = self._intensity(observations[-1])
        is_light_on = self._is_light_on(observations)

    def _intensity(self, latest: LightObservation) -> float:
        raw_adc = latest.payload.raw_adc
        bright = self.policies.light.calibration.adc.bright
        dark = self.policies.light.calibration.adc.dark

        normalized = (raw_adc - dark) / (bright - dark)
        return max(0.0, min(1.0, normalized))

    def _is_light_on(self, observations: list[LightObservation]) -> bool:
        ...

    def _state_started_at(self) -> datetime: 
        ...
