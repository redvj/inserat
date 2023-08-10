# Reste password Request

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from flask_wtf import FlaskForm
from flask_mail import Message
from app import mail


# Form for requesting a password reset
class ResetPasswordRequestForm(FlaskForm):
    # Input field for the email address with DataRequired and Email validators
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Submit button to initiate the password reset request
    submit = SubmitField('Request Password Reset')

# Form for resetting the password
class ResetPasswordForm(FlaskForm):
    # Password field for the new password with DataRequired validator
    password = PasswordField('Password', validators=[DataRequired()])
    # Password field for confirming the new password with DataRequired and EqualTo('password') validators
    # to ensure that the password is repeated correctly
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # Submit button to initiate the password reset
    submit = SubmitField('Request Password Reset')