from peewee import Model
from .db import db


class BaseDbModel(Model):

    class Meta:
        database = db
