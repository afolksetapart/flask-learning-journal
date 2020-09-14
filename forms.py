from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Regexp, Email, Length, EqualTo, ValidationError

from models import User
import datetime


def check_for_username(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Sorry! That username is already taken.')


def check_for_email(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('Sorry! That email is already in our system.')


class EntryForm(Form):
    title = StringField('Subject', validators=[DataRequired()])
    date = DateField(default=datetime.datetime.now)
    time_spent = StringField('Minutes Spent Learning',
                             validators=[DataRequired(),
                                         Regexp(
                                 r'^[0-9]+$',
                                 message=(
                                     'Time should be entered in minutes '
                                     'and only contain numbers 0-9'))])
    learned = TextAreaField('What did you learn?',
                            validators=[DataRequired()])
    resources = TextAreaField('Resources')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(Form):
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp(
            r'^[a-zA-Z0-9_]+$',
            message=('Sorry! Usernames can only include numbers, '
                     'letters and/or underscores.')),
        Length(max=10,
               message='Sorry! Usernames can '
               'only be up to 10 characters.'),
        check_for_username
    ])
    email = StringField('E-mail', validators=[
        DataRequired(),
        Email(),
        check_for_email
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters.'),
        EqualTo('password2', message='Passwords must match.')
    ])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
