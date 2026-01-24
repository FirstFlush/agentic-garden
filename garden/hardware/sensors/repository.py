from datetime import datetime
import logging
import orjson
from peewee import ModelSelect
from typing import Iterator
from .models import SensorReading
from .schemas import SensorReadingSchema
from .enums import SensorType
from .exc import SensorError

logger = logging.getLogger(__name__)


class SensorReadingRepository:

    def save_reading(self, schema: SensorReadingSchema) -> SensorReading:
        try:
            return SensorReading.create(
                observed_at=schema.created,
                sensor_type=schema.sensor_type.value,
                sensor_id=schema.sensor_id,
                payload=orjson.dumps(schema.payload).decode("utf-8"),
            )
        except orjson.JSONEncodeError as e:
            msg = f"Failed to serialize JSON for SensorReading record creation due to the following error: {e}"
            self._raise_error(msg, e)
        except Exception as e:
            msg = f"Failed to create SensorReading record due to the following error: {e}"
            self._raise_error(msg, e)    

    def fetch_readings(
            self,
            sensor_type: SensorType,
            sensor_id: str,
            window_start: datetime,
            window_end: datetime,
    ) -> list[SensorReadingSchema]:
        try:
            rows = (
                SensorReading
                .select()
                .where(
                    (SensorReading.sensor_type == sensor_type.value) &
                    (SensorReading.sensor_id == sensor_id) &
                    SensorReading.created.between(window_start, window_end)
                )
                .order_by(SensorReading.created)
            )

            return [
                SensorReadingSchema(
                    created=row.created,
                    sensor_type=row.sensor_type,
                    sensor_id=row.sensor_id,
                    payload=orjson.loads(row.payload),
                )
                for row in rows
            ]
        except orjson.JSONDecodeError as e:
            msg = f"Failed to deserialize JSON for SensorReading records due to the following error: {e}"
            self._raise_error(msg, e)
        except Exception as e:
            msg = f"Failed to fetch SensorReading records due to the following error: {e}"
            self._raise_error(msg, e)

    def fetch_latest_reading(
            self,
            sensor_type: SensorType,
            sensor_id: str,
    ) -> SensorReadingSchema | None:
        try:
            row = (
                SensorReading
                .select()
                .where(
                    (SensorReading.sensor_type == sensor_type.value) &
                    (SensorReading.sensor_id == sensor_id)
                )
                .order_by(SensorReading.created.desc())
                .first()
            )

            if not row:
                return None

            return SensorReadingSchema(
                created=row.created,
                sensor_type=row.sensor_type,
                sensor_id=row.sensor_id,
                payload=orjson.loads(row.payload),
            )
        except orjson.JSONDecodeError as e:
            msg = f"Failed to deserialize JSON for SensorReading record due to the following error: {e}"
            self._raise_error(msg, e)
        except Exception as e:
            msg = f"Failed to fetch latest SensorReading record due to the following error: {e}"
            self._raise_error(msg, e)

    def iter_readings(
            self,
            sensor_type: SensorType,
            sensor_id: str,
            window_start: datetime,
            window_end: datetime,
    ) -> Iterator[SensorReadingSchema]:
        """
        Iterate over raw sensor sensor readings within a given time window.

        This is the streaming counterpart to fetch_readings(), yielding
        SensorReadingSchema objects one at a time instead of materializing
        the full result set in memory. Intended for large result sets or
        memory-sensitive processing.
        """
        try:
            query: ModelSelect = (
                SensorReading
                .select()
                .where(
                    (SensorReading.sensor_type == sensor_type.value) &
                    (SensorReading.sensor_id == sensor_id) &
                    SensorReading.created.between(window_start, window_end)
                )
                .order_by(SensorReading.created)
            )

            for row in query.iterator():
                yield SensorReadingSchema(
                    created=row.created,
                    sensor_type=row.sensor_type,
                    sensor_id=row.sensor_id,
                    payload=orjson.loads(row.payload),
                )
        except orjson.JSONDecodeError as e:
            msg = f"Failed to deserialize JSON for SensorReading records due to the following error: {e}"
            self._raise_error(msg, e)
        except Exception as e:
            msg = f"Failed to iterate SensorReading records due to the following error: {e}"
            self._raise_error(msg, e)

    def _raise_error(self, msg: str, e: Exception):
        logger.error(msg, exc_info=True)
        raise SensorError(msg) from e
