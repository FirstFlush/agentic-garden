from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = ROOT_DIR / "garden"
STORAGE_DIR = APP_DIR / "storage"

DB_PATH = STORAGE_DIR / "db.sqlite3"

SENSORS_CONFIG_PATH = ROOT_DIR / "sensors.yaml"
POLICIES_CONFIG_PATH = ROOT_DIR / "policies.yaml"