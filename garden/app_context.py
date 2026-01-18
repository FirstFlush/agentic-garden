from dataclasses import dataclass
from peewee import SqliteDatabase
from .config.sensors import SensorsConfig
from .config.policies import PoliciesConfig

@dataclass(frozen=True)
class AppContext:
    """
    Central runtime context for the application.

    AppContext holds shared, read-only objects that are constructed once
    at startup (e.g. loaded configuration and database connection) and
    are required across multiple parts of the system.

    In CLI execution, an AppContext instance is attached to the Typer
    runtime context (ctx.obj) and explicitly passed into commands and
    services that need access to global application state.
    """
    sensors_config: SensorsConfig
    policies_config: PoliciesConfig
    db: SqliteDatabase
