from peewee import (
    AutoField,
    TextField,
)
from playhouse.sqlite_ext import JSONField
from ...db.base import BaseDBModel


class SensorReading(BaseDBModel):
    id = AutoField()
    sensor_type = TextField(index=True)
    sensor_id = TextField(index=True)
    payload = JSONField()

    class Meta:  # type: ignore[misc]
        table_name = "sensor_reading"
