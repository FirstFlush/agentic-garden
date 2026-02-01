from playhouse.sqlite_ext import JSONField
from peewee import (
    AutoField,
    FloatField,
    TextField,
)
from ..db.base import BaseDBModel
from .enums import DecisionOutcome


class DecisionLog(BaseDBModel):

    id = AutoField()
    decision_outcome = TextField(choices=DecisionOutcome.choices, index=True)
    confidence = FloatField()
    derived_state = JSONField()
    policy_version = TextField(index=True)

    class Meta:  # type: ignore[misc]
        table_name = "decision_log"
