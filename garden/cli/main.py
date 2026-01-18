import logging
import logging.config
import typer
from dotenv import load_dotenv
from garden.config.logging import LOGGING

logger = logging.getLogger(__name__)
app = typer.Typer(add_completion=False)


def bootstrap():
    load_dotenv()
    logging.config.dictConfig(LOGGING)
    logger.info("CLI bootstrap complete")


@app.command()
def test(name: str = "world"):
    logger = logging.getLogger(__name__)
    logger.info("test command invoked")
    typer.echo(f"hello {name}")


def main():
    bootstrap()
    app()


if __name__ == "__main__":
    main()
