import logging
import logging.config
import typer
from dotenv import load_dotenv
from peewee import SqliteDatabase
from ..config.constants import SENSORS_CONFIG_PATH, POLICIES_CONFIG_PATH
from ..config.logging import LOGGING
from ..config.sensors import load_sensors_config
from ..config.policies import load_policies_config
from ..storage.db import db
from ..storage.models import RawObservation
from ..app_context import AppContext

logger = logging.getLogger(__name__)
app = typer.Typer(add_completion=False)


def init_db(db: SqliteDatabase):
    db.connect(reuse_if_open=True)
    db.create_tables([RawObservation], safe=True)
    logger.info("Established DB connection")

def build_app_context(db: SqliteDatabase) -> AppContext:
    app_context = AppContext(
        sensors_config=load_sensors_config(SENSORS_CONFIG_PATH),
        policies_config=load_policies_config(POLICIES_CONFIG_PATH),
        db=db,
    )
    logger.info("Built AppContext object")
    return app_context

def bootstrap():
    load_dotenv()
    logging.config.dictConfig(LOGGING)
    init_db(db)
    logger.info("CLI bootstrap complete")


@app.command()
def test(ctx: typer.Context, name: str = "world"):


    print(ctx.obj)

    logger.info("test command invoked")

    typer.echo(f"hello {name}")


def main():
    bootstrap()
    app_context = build_app_context(db)

    @app.callback()
    def root(ctx: typer.Context):
        ctx.obj = app_context
    app()


if __name__ == "__main__":
    main()
