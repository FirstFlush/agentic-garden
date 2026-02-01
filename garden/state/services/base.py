from abc import ABC
import logging
from typing import Sequence
from ...common.types import HasCreated
from ...config.policies import PoliciesConfig
from ...hardware.sensors.schemas import SensorPayload
from ...hardware.sensors.schemas import SensorReadingSchema
from ...hardware.sensors.dto import ParsedSensorReading
from ..dto import EvidenceWindow
from ..exc import StateServiceException

logger = logging.getLogger(__name__)


class BaseStateService(ABC):

    def __init__(self, policies: PoliciesConfig):
        self.policies = policies

    def confidence_score(self, window: EvidenceWindow, min_samples: int) -> float:
        """
        Compute an evidence-based confidence score for a derived state.

        Confidence reflects how much evidence is available relative to the
        minimum required to form a stable belief. It is defined as the ratio
        of observed samples to the configured minimum sample count, capped
        at 1.0 once the evidence requirement is satisfied.

        This is not a statistical probability. It is a policy-aligned measure
        of evidentiary sufficiency, intended for debouncing, conservative
        decision-making, and downstream action gating.
        """
        return min(1.0, window["sample_count"] / min_samples)

    def evidence_window(self, sensor_readings: Sequence[HasCreated]) -> EvidenceWindow:
        return EvidenceWindow(
            window_start=sensor_readings[0].created,
            window_end=sensor_readings[-1].created,
            sample_count=len(sensor_readings),
        )

    def parse_sensor_readings(
            self,
            sensor_readings: list[SensorReadingSchema],
            payload_schema: type[SensorPayload],
    ) -> list[ParsedSensorReading]:
        parsed = []
        for obv in sensor_readings:
            try:
                payload = payload_schema(**obv.payload)
            except Exception as e:
                msg = f"Invalid payload for sensor {obv.sensor_id}: {e}"
                logger.error(msg, exc_info=True)
                raise StateServiceException(msg) from e

            parsed.append(
                ParsedSensorReading(
                    created=obv.created,
                    sensor_type=obv.sensor_type,
                    sensor_id=obv.sensor_id,
                    payload=payload,
                )
            )
        return parsed
