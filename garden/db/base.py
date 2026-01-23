from datetime import datetime, UTC
from peewee import Model
from peewee import DateTimeField, IntegerField, FloatField
from .sqlite_db import db


class BaseDBModel(Model):

    created = DateTimeField(index=True, default=lambda: datetime.now(UTC))

    class Meta:
        database = db
        abstract = True


class StateModel(BaseDBModel):

    window_start =  DateTimeField()
    window_end = DateTimeField()
    sample_count = IntegerField()
    confidence = FloatField()

    class Meta: # type: ignore[misc]
        abstract = True
