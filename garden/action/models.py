from peewee import (
    AutoField,
    TextField,
    BooleanField,
)
from garden.db.base import BaseDBModel


class ActionLog(BaseDBModel):
    """
    Records every attempted or executed action taken by the system.
    This is the system's behavioral memory.
    """
    id = AutoField()
    action_type = TextField(index=True)
    actuator_id = TextField(index=True)
    action_params = TextField(null=True)        # JSON
    requested_by = TextField()
    # decision_facts = TextField(null=True)     # JSON
    state_snapshot = TextField(null=True)       # JSON 
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
