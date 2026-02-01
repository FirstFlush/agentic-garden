from datetime import datetime
from playhouse.sqlite_ext import JSONField
from peewee import (
    AutoField,
    FloatField,
    TextField,
)
from ..db.base import BaseDBModel
from .enums import DecisionOutcome, EscalationTarget


class DecisionLog(BaseDBModel):

    id = AutoField()
    decision_outcome = TextField(choices=DecisionOutcome.choices, index=True)
    escalation_target = TextField(choices=EscalationTarget.choices, null=True) # no-action has no escalation target 
    confidence = FloatField()
    reasons = JSONField()
    derived_state = JSONField()
    policy_version = TextField(index=True)

    class Meta: # type: ignore[misc]
        table_name = "decision_log"
