from peewee import Model
from .db import db


class BaseDBModel(Model):

    class Meta:
        database = db
