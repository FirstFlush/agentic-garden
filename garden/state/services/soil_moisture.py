import logging
from .base import BaseStateService
from ..schemas import SoilMoistureStateSchema
from ..exc import StateServiceException
from ..enums import SoilMoistureLevel, SoilMoistureTrend
from ...hardware.sensors.dto import SoilMoistureReading

logger = logging.getLogger(__name__)


class SoilMoistureStateService(BaseStateService):

    def derive_state(
        self,
        sensor_readings: list[SoilMoistureReading],
    ) -> SoilMoistureStateSchema:

        if not sensor_readings:
            msg = f"{self.__class__.__name__} received 0 sensor readings"
            logger.error(msg)
            raise StateServiceException(msg)

        window = self.evidence_window(sensor_readings)

        confidence = self.confidence_score(
            window=window,
            min_samples=self.policies.soil_moisture.interpretation.level.min_samples,
        )

        avg_moisture = self._avg_moisture(sensor_readings)
        level = self._level(avg_moisture)
        trend = self._trend(sensor_readings)

        return SoilMoistureStateSchema(
            avg_moisture=avg_moisture,
            level=level,
            trend=trend,
            confidence=confidence,
            **window,
        )

    def _normalize(self, raw_adc: int) -> float:
        """
        Normalize raw ADC reading to 0–1 moisture scale.
        0.0 = fully dry
        1.0 = fully wet
        """
        dry = self.policies.soil_moisture.calibration.adc.dry
        wet = self.policies.soil_moisture.calibration.adc.wet

        # Inverted sensor: higher ADC = drier
        normalized = (dry - raw_adc) / (dry - wet)
        return max(0.0, min(1.0, normalized))

    def _avg_moisture(
        self,
        sensor_readings: list[SoilMoistureReading],
    ) -> float:
        values = [
            self._normalize(r.payload.raw_adc)
            for r in sensor_readings
        ]
        return sum(values) / len(values)

    def _level(self, avg_moisture: float) -> SoilMoistureLevel:
        cfg = self.policies.soil_moisture.interpretation.level

        if avg_moisture <= cfg.dry_threshold:
            return SoilMoistureLevel.DRY

        if avg_moisture >= cfg.wet_threshold:
            return SoilMoistureLevel.WET

        return SoilMoistureLevel.OK

    def _trend(
        self,
        sensor_readings: list[SoilMoistureReading],
    ) -> SoilMoistureTrend:
        cfg = self.policies.soil_moisture.interpretation.trend
        N = cfg.lookback_samples

        if len(sensor_readings) < N:
            return SoilMoistureTrend.STABLE

        values = [
            self._normalize(r.payload.raw_adc)
            for r in sensor_readings[-N:]
        ]

        delta = values[-1] - values[0]

        if delta >= cfg.min_delta:
            return SoilMoistureTrend.WETTING

        if delta <= -cfg.min_delta:
            return SoilMoistureTrend.DRYING

        return SoilMoistureTrend.STABLE
