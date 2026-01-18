from datetime import datetime
import logging
import orjson
from peewee import ModelSelect
from typing import Iterator
from .exc import StorageServiceException
from .models import RawObservation
from .schemas import RawObservationSchema
from ..hardware.enums import SensorType

logger = logging.getLogger(__name__)


class StorageService:

    def save_observation(self, schema: RawObservationSchema) -> RawObservation:
        try:
            return RawObservation.create(
                observed_at=schema.created,
                sensor_type=schema.sensor_type.value,
                sensor_id=schema.sensor_id,
                payload=orjson.dumps(schema.payload).decode("utf-8"),
            )
        except Exception as e:
            msg = f"Failed to create RawObservation record due to the following error: {e}"
            self._raise_error(msg, e)    

    def fetch_observations(
            self,
            sensor_type: SensorType,
            sensor_id: str,
            window_start: datetime,
            window_end: datetime,
    ) -> list[RawObservationSchema]:
        try:
            rows = (
                RawObservation
                .select()
                .where(
                    (RawObservation.sensor_type == sensor_type.value) &
                    (RawObservation.sensor_id == sensor_id) &
                    RawObservation.created.between(window_start, window_end)
                )
                .order_by(RawObservation.created)
            )

            return [
                RawObservationSchema(
                    created=row.created,
                    sensor_type=row.sensor_type,
                    sensor_id=row.sensor_id,
                    payload=orjson.loads(row.payload),
                )
                for row in rows
            ]
        except Exception as e:
            msg = f"Failed to fetch RawObservation records due to the following error: {e}"
            self._raise_error(msg, e)

    def fetch_latest(
            self,
            sensor_type: SensorType,
            sensor_id: str,
    ) -> RawObservationSchema | None:
        try:
            row = (
                RawObservation
                .select()
                .where(
                    (RawObservation.sensor_type == sensor_type.value) &
                    (RawObservation.sensor_id == sensor_id)
                )
                .order_by(RawObservation.created.desc())
                .first()
            )

            if not row:
                return None

            return RawObservationSchema(
                created=row.created,
                sensor_type=row.sensor_type,
                sensor_id=row.sensor_id,
                payload=orjson.loads(row.payload),
            )
        except Exception as e:
            msg = f"Failed to fetch latest RawObservation record due to the following error: {e}"
            self._raise_error(msg, e)

    def iter_observations(
            self,
            sensor_type: SensorType,
            sensor_id: str,
            window_start: datetime,
            window_end: datetime,
    ) -> Iterator[RawObservationSchema]:
        """
        Iterate over raw sensor observations within a given time window.

        This is the streaming counterpart to fetch_observations(), yielding
        RawObservationSchema objects one at a time instead of materializing
        the full result set in memory. Intended for large result sets or
        memory-sensitive processing.
        """
        try:
            query: ModelSelect = (
                RawObservation
                .select()
                .where(
                    (RawObservation.sensor_type == sensor_type.value) &
                    (RawObservation.sensor_id == sensor_id) &
                    RawObservation.created.between(window_start, window_end)
                )
                .order_by(RawObservation.created)
            )

            for row in query.iterator():
                yield RawObservationSchema(
                    created=row.created,
                    sensor_type=row.sensor_type,
                    sensor_id=row.sensor_id,
                    payload=orjson.loads(row.payload),
                )
        except Exception as e:
            msg = f"Failed to iterate RawObservation records due to the following error: {e}"
            self._raise_error(msg, e)

    def _raise_error(self, msg: str, e: Exception):
        logger.error(msg, exc_info=True)
        raise StorageServiceException(msg) from e
