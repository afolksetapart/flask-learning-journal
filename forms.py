from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Regexp, Email


class EntryForm(Form):
    title = StringField('Subject', validators=[DataRequired()])
    time_spent = IntegerField('Minutes Spent Learning',
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
