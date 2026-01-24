from abc import ABC, abstractmethod
import logging
from ...config.policies import PoliciesConfig
from ...hardware.schemas import SensorPayload
from ...observations.schemas import RawObservationSchema
from ...observations.service import ObservationService
from ...observations.dto import ParsedObservation
from ..exc import StateServiceException
from ..schemas import DerivedStateSchema

logger = logging.getLogger(__name__)


class BaseStateService(ABC):

    def __init__(self, policies: PoliciesConfig):
        self.policies = policies

    def parse_observations(
            self,
            observations: list[RawObservationSchema],
            payload_schema: type[SensorPayload],
    ) -> list[ParsedObservation]:
        parsed = []
        for obv in observations:
            try:
                payload = payload_schema(**obv.payload)
            except Exception as e:
                msg = f"Invalid payload for sensor {obv.sensor_id}: {e}"
                logger.error(msg, exc_info=True)
                raise StateServiceException(msg) from e

            parsed.append(
                ParsedObservation(
                    created=obv.created,
                    sensor_type=obv.sensor_type,
                    sensor_id=obv.sensor_id,
                    payload=payload,
                )
            )
        return parsed
