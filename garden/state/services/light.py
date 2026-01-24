from datetime import datetime
import logging
from .base import BaseStateService
from ..exc import StateServiceException
from ..schemas import LightStateSchema
from ...hardware.sensors.dto import LightReading

logger = logging.getLogger(__name__)


class LightStateService(BaseStateService):

    def derive_state(
            self, 
            sensor_readings: list[LightReading], 
            previous_state: LightStateSchema | None
    ) -> LightStateSchema:
        
        if not sensor_readings:
            msg = f"{self.__class__.__name__} received 0 sensor readings"
            logger.error(msg)
            raise StateServiceException(msg)

        window = self.evidence_window(sensor_readings)
        confidence = self.confidence_score(
            window=window,
            min_samples=self.policies.light.interpretation.on_off.min_samples,
        )
        intensity = self._intensity(sensor_readings[-1])
        is_light_on = self._is_light_on(sensor_readings, previous_state=previous_state)
        state_started_at = self._state_started_at(
            is_light_on=is_light_on,
            previous_state=previous_state,
            window_end=window["window_end"]
        )
        return LightStateSchema(
            intensity=intensity,
            is_light_on=is_light_on,
            state_started_at=state_started_at,
            confidence=confidence,
            **window,
        )

    def _intensity(self, latest: LightReading) -> float:
        raw_adc = latest.payload.raw_adc
        bright = self.policies.light.calibration.adc.bright
        dark = self.policies.light.calibration.adc.dark

        normalized = (raw_adc - dark) / (bright - dark)
        return max(0.0, min(1.0, normalized))

    def _is_light_on(
        self,
        sensor_readings: list[LightReading],
        previous_state: LightStateSchema | None,
    ) -> bool:
        cfg = self.policies.light.interpretation.on_off
        N = cfg.min_samples

        if len(sensor_readings) < N:
            return previous_state.is_light_on if previous_state else False

        values = [
            self._intensity(obs)
            for obs in sensor_readings[-N:]
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

    def _state_started_at(
            self,
            is_light_on: bool,
            previous_state: LightStateSchema | None,
            window_end: datetime,
    ) -> datetime:
        if previous_state is None:
            return window_end

        if previous_state.is_light_on == is_light_on:
            return previous_state.state_started_at

        return window_end