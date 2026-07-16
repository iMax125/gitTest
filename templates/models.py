from peewee import *

db = SqliteDatabase('db.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    name = CharField(unique=True)
    price = FloatField()
    category = CharField()


def init_db():
    db.connect()
    db.create_tables([Product])
