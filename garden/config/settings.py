import logging
import logging.config
from pathlib import Path
from .logging import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = ROOT_DIR / "garden"
STORAGE_DIR = APP_DIR / "storage"

DB_PATH = STORAGE_DIR / "db.sqlite3"
