import logging
import logging.config
import typer
from dotenv import load_dotenv
from ..config.logging import LOGGING
from ..storage.db import db
from ..storage.models import RawObservation

logger = logging.getLogger(__name__)
app = typer.Typer(add_completion=False)


def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables([RawObservation], safe=True)
    logger.info("Established DB connection")


def bootstrap():
    load_dotenv()
    logging.config.dictConfig(LOGGING)
    init_db()
    logger.info("CLI bootstrap complete")


@app.command()
def test(name: str = "world"):
    logger.info("test command invoked")
    typer.echo(f"hello {name}")


def main():
    bootstrap()
    app()


if __name__ == "__main__":
    main()
