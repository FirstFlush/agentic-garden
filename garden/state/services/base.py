from abc import ABC, abstractmethod
import logging
from typing import Type
from ...hardware.schemas import SensorPayload
from ...observations.schemas import RawObservationSchema
from ...observations.service import ObservationService
from ...observations.dto import ParsedObservation
from ..exc import StateServiceException
from ..schemas import DerivedStateSchema

logger = logging.getLogger(__name__)


class BaseStateService(ABC):

    def __init__(self, observation_service: ObservationService):
        self.observation_service = observation_service

    @abstractmethod
    def derive_state(self, observations: list[ParsedObservation]) -> DerivedStateSchema:
        ...

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
