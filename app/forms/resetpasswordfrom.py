# Reste password Request

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from flask_wtf import FlaskForm
from flask_mail import Message
from app import mail



class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')