from abc import ABC, abstractmethod
import logging
import orjson
from typing import Any, cast, Generic, TypeVar, Type
from ...hardware.schemas import SensorPayload
from ...storage.schemas import RawObservationSchema
from ...storage.service import StorageService
from ..dto import ParsedObservation
from ..exc import StateServiceException
from ..schemas import DerivedState

logger = logging.getLogger(__name__)

P = TypeVar("P", bound=SensorPayload)
S = TypeVar("S", bound=DerivedState)

class BaseStateService(ABC, Generic[P, S]):

    _payload_schema: Type[P]
    _state_schema: Type[S]

    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service
        try:
            self._payload_schema
            self._state_schema
        except AttributeError as e:
            msg = f"{self.__class__.__name__} misconfigured: missing schema definition"
            logger.error(msg, exc_info=True)
            raise StateServiceException(msg) from e

    def derive_state(self, observations: list[RawObservationSchema]) -> S:
        """
        DO NOT override in subclasses.
        Override _derive_state only.
        """
        parsed_observations = self._parse_observations(observations)
        try:
            return self._derive_state(parsed_observations)
        except StateServiceException:
            raise 
        except Exception as e:
            msg = f"{self.__class__.__name__} failed to derive state due to an unexpected error: {e}"
            logger.error(msg, exc_info=True)
            raise StateServiceException(msg) from e

    @abstractmethod
    def _derive_state(self, observations: list[ParsedObservation[P]]) -> S:
        ...

    def _parse_observations(self, observations: list[RawObservationSchema]) -> list[ParsedObservation[P]]:
        parsed_obvs: list[ParsedObservation[P]] = []
        for obv in observations:
            payload = self._parse_payload(obv.payload)
            parsed_obv = ParsedObservation(
                created=obv.created,
                sensor_type=obv.sensor_type,
                sensor_id=obv.sensor_id,
                payload=payload
            )
            parsed_obvs.append(parsed_obv)
        return parsed_obvs

    def _parse_payload(self, payload: dict[str, Any]) -> P:
        try:
            return self._payload_schema(**payload)
        except Exception as e:
            msg = f"{self.__class__.__name__} payload schema validation failed due to the following error: {e}"
            logger.error(msg, exc_info=True)
            raise StateServiceException(msg) from e
            


    # def _deserialize_payload(self, payload: str) -> dict[str, Any]:
    #     try:
    #         return orjson.loads(payload)
    #     except orjson.JSONDecodeError as e:
    #         msg = f"{self.__class__.__name__} JSON deserialization failed due to the following error: {e}"
    #         logger.error(msg, exc_info=True)
    #         raise StateServiceException(msg) from e
