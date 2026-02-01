from peewee import (
    AutoField,
    TextField,
    BooleanField,
    ForeignKeyField
)
from playhouse.sqlite_ext import JSONField
from garden.db.base import BaseDBModel
from ..decision.models import DecisionLog


class ActionLog(BaseDBModel):
    """
    Records every attempted or executed action taken by the system.
    This is the system's behavioral memory.
    """
    id = AutoField()
    action_type = TextField(index=True)
    actuator_id = TextField(index=True)
    action_params = JSONField(null=True)
    requested_by = TextField()
    decision = ForeignKeyField(DecisionLog, backref="decisions", on_delete="CASCADE")
    approved = BooleanField(default=False)
    executed = BooleanField(default=False)

    result = TextField(null=True)
    error_message = TextField(null=True)

    class Meta: # type: ignore[misc]
        table_name = "action_log"
        indexes = (
            (("action_type", "created"), False),
            (("actuator_id", "created"), False),
            (("requested_by", "created"), False),
        )
