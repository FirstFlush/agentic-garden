from peewee import SqliteDatabase
from garden.config.settings import DB_PATH

db = SqliteDatabase(
    DB_PATH,
    pragmas={
        "journal_mode": "wal",
        "foreign_keys": 1,
    },
)
