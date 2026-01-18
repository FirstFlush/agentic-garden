from datetime import datetime, UTC
from peewee import (
    AutoField,
    TextField,
    DateTimeField,
)
from .base import BaseDBModel


class RawObservation(BaseDBModel):
    id = AutoField()
    sensor_type = TextField(index=True)
    sensor_id = TextField(index=True)
    payload = TextField()
    created = DateTimeField(index=True, default=lambda: datetime.now(UTC))

    class Meta(BaseDBModel.Meta):
        table_name = "raw_observations"
