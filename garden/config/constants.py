from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = ROOT_DIR / "garden"

DB_DIR = APP_DIR / "db"
DB_PATH = DB_DIR / "db.sqlite3"

SENSORS_CONFIG_PATH = ROOT_DIR / "sensors.yaml"
POLICIES_CONFIG_PATH = ROOT_DIR / "policies.yaml"