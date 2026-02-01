from datetime import datetime
from peewee import ModelSelect
from typing import Iterator
from .models import SensorReading
from .schemas import SensorReadingSchema
from .enums import SensorType
from ...common.exc import RepositoryError


class SensorReadingRepository:

    def save_reading(self, schema: SensorReadingSchema) -> SensorReading:
        try:
            return SensorReading.create(
                created=schema.created,
                sensor_type=schema.sensor_type.value,
                sensor_id=schema.sensor_id,
                payload=schema.payload,
            )
        except Exception as e:
            msg = f"Failed to create SensorReading record due to the following error: {e}"
            raise RepositoryError(msg) from e    

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
                    payload=row.payload,
                )
                for row in rows
            ]
        except Exception as e:
            msg = f"Failed to fetch SensorReading records due to the following error: {e}"
            raise RepositoryError(msg) from e

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
                payload=row.payload,
            )
        except Exception as e:
            msg = f"Failed to fetch latest SensorReading record due to the following error: {e}"
            raise RepositoryError(msg) from e

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
                    payload=row.payload,
                )
        except Exception as e:
            msg = f"Failed to iterate SensorReading records due to the following error: {e}"
            raise RepositoryError(msg) from e
