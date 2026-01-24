from abc import ABC
import logging
from ...config.policies import PoliciesConfig
from ...hardware.sensors.schemas import SensorPayload
from ...hardware.sensors.schemas import SensorReadingSchema
from ...hardware.sensors.dto import ParsedSensorReading
from ..exc import StateServiceException

logger = logging.getLogger(__name__)


class BaseStateService(ABC):

    def __init__(self, policies: PoliciesConfig):
        self.policies = policies

    def parse_observations(
            self,
            observations: list[SensorReadingSchema],
            payload_schema: type[SensorPayload],
    ) -> list[ParsedSensorReading]:
        parsed = []
        for obv in observations:
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
