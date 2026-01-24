from datetime import datetime, UTC
from peewee import (
    AutoField,
    TextField,
)
from ...db.base import BaseDBModel


class SensorReading(BaseDBModel):
    id = AutoField()
    sensor_type = TextField(index=True)
    sensor_id = TextField(index=True)
    payload = TextField()

    class Meta:  # type: ignore[misc]
        table_name = "sensor_reading"
