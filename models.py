import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase("plants.sqlite")


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class Plant(Model):
    name = CharField()
    scientific_name = CharField(null=True)
    owner = ForeignKeyField(User, backref="plants")
    image = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Plant, User], safe=True)
    print("Tables Created")
    DATABASE.close()
