from peewee import (
    AutoField,
    TextField,
    DateTimeField,
)
from .base import BaseDbModel


class RawObservation(BaseDbModel):
    id = AutoField()
    observed_at = DateTimeField(index=True)
    sensor_type = TextField(index=True)
    sensor_id = TextField(index=True)
    payload = TextField()

    class Meta(BaseDbModel.Meta):
        table_name = "raw_observations"
