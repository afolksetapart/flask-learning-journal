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
        try:
            with db.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("Sorry! A user with that name already exists!")

    class Meta:
        database = db


class Entry(Model):
    title = CharField()
    user = ForeignKeyField(
        User,
        related_name='entries'
    )
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField(default='')
    tag_string = TextField(default='')

    class Meta:
        database = db


class Tag(Model):
    tag = CharField()
    entry = ForeignKeyField(Entry, related_name='tags')

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([User, Entry, Tag], safe=True)
    db.close()
