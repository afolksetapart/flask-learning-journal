import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from peewee import *

db = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)

    @classmethod
    def make_user(cls, username, email, password):
        cls.create(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

    class Meta:
        database = db


class Entry(Model):
    title = CharField()
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField(default='')

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([User, Entry], safe=True)
    db.close()
