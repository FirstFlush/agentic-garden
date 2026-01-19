from peewee import Model
from .sqlite_db import db


class BaseDBModel(Model):

    class Meta:
        database = db
