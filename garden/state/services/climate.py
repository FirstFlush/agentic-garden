import logging
from .base import BaseStateService
from ..schemas import ClimateStateSchema
from ..exc import StateServiceException
from ..enums import (
    TemperatureLevel,
    TemperatureTrend,
    HumidityLevel,
    HumidityTrend,
)
from ...hardware.sensors.dto import ClimateReading

logger = logging.getLogger(__name__)


class ClimateStateService(BaseStateService):

    def derive_state(
        self,
        sensor_readings: list[ClimateReading],
    ) -> ClimateStateSchema:

        if not sensor_readings:
            msg = f"ClimateStateService received 0 sensor readings"
            logger.error(msg)
            raise StateServiceException(msg)

        window = self.evidence_window(sensor_readings)

        confidence = self.confidence_score(
            window=window,
            min_samples=self.policies.climate.interpretation.temperature.hysteresis.min_samples,
        )

        latest = sensor_readings[-1].payload

        temperature_level = self._temperature_level(latest.temp)
        humidity_level = self._humidity_level(latest.humidity)

        temperature_trend = self._temperature_trend(sensor_readings)
        humidity_trend = self._humidity_trend(sensor_readings)

        return ClimateStateSchema(
            temperature_c=latest.temp,
            humidity_rh=latest.humidity,
            vpd_kpa=None,
            temperature_level=temperature_level,
            temperature_trend=temperature_trend,
            humidity_level=humidity_level,
            humidity_trend=humidity_trend,
            confidence=confidence,
            **window,
        )

    def _temperature_level(self, value_c: float) -> TemperatureLevel:
        cfg = self.policies.climate.interpretation.temperature.acceptable
        if value_c < cfg.min_c:
            return TemperatureLevel.TOO_COLD
        if value_c > cfg.max_c:
            return TemperatureLevel.TOO_HOT
        return TemperatureLevel.OK

    def _humidity_level(self, value_rh: float) -> HumidityLevel:
        cfg = self.policies.climate.interpretation.humidity.acceptable
        if value_rh < cfg.min_percent:
            return HumidityLevel.TOO_DRY
        if value_rh > cfg.max_percent:
            return HumidityLevel.TOO_HUMID
        return HumidityLevel.OK

    def _temperature_trend(
        self,
        sensor_readings: list[ClimateReading],
    ) -> TemperatureTrend:
        N = self.policies.climate.interpretation.temperature.hysteresis.min_samples
        if len(sensor_readings) < N:
            return TemperatureTrend.STABLE

        values = [r.payload.temp for r in sensor_readings[-N:]]
        delta = values[-1] - values[0]
        min_delta = self.policies.climate.interpretation.trends.min_delta.temperature_c

        if delta >= min_delta:
            return TemperatureTrend.HEATING
        if delta <= -min_delta:
            return TemperatureTrend.COOLING
        return TemperatureTrend.STABLE

    def _humidity_trend(
        self,
        sensor_readings: list[ClimateReading],
    ) -> HumidityTrend:
        N = self.policies.climate.interpretation.humidity.hysteresis.min_samples
        if len(sensor_readings) < N:
            return HumidityTrend.STABLE

        values = [r.payload.humidity for r in sensor_readings[-N:]]
        delta = values[-1] - values[0]
        min_delta = self.policies.climate.interpretation.trends.min_delta.humidity_percent

        if delta >= min_delta:
            return HumidityTrend.HUMIDIFYING
        if delta <= -min_delta:
            return HumidityTrend.DRYING
        return HumidityTrend.STABLE
