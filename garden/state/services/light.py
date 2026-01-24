from datetime import datetime
import logging
from .base import BaseStateService
from ..models import LightState
from ..schemas import LightStateSchema
from ...hardware.sensors.schemas import LightPayload
from ...hardware.sensors.dto import LightObservation
from ...hardware.sensors.schemas import SensorReadingSchema


logger = logging.getLogger(__name__)


class LightStateService(BaseStateService):

    def derive_state(self, observations: list[LightObservation], previous_state: LightStateSchema | None) -> LightStateSchema:
        intensity = self._intensity(observations[-1])
        is_light_on = self._is_light_on(observations, previous_state=previous_state)
        state_started_at = self._state_started_at(previous_state)
        return LightStateSchema(
            intensity=intensity,
            is_light_on=is_light_on,
            state_started_at=state_started_at,
        )

    def _intensity(self, latest: LightObservation) -> float:
        raw_adc = latest.payload.raw_adc
        bright = self.policies.light.calibration.adc.bright
        dark = self.policies.light.calibration.adc.dark

        normalized = (raw_adc - dark) / (bright - dark)
        return max(0.0, min(1.0, normalized))

    def _is_light_on(
        self,
        observations: list[LightObservation],
        previous_state: LightStateSchema | None,
    ) -> bool:
        cfg = self.policies.light.interpretation.on_off
        N = cfg.min_samples

        if len(observations) < N:
            return previous_state.is_light_on if previous_state else False

        values = [
            self._intensity(obs)
            for obs in observations[-N:]
        ]

        all_high = all(v >= cfg.on_threshold for v in values)
        all_low  = all(v <= cfg.off_threshold for v in values)

        if previous_state is None:
            # bootstrap conservatively
            return all_high

        if previous_state.is_light_on:
            return False if all_low else True
        else:
            return True if all_high else False


    def _state_started_at(self, previous_state: LightStateSchema | None) -> datetime: 
        if previous_state is None:
            return datetime.now()
        

        