from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models.login import User


#Übernommen aus den Beispielen Microblog


# Form for user login
class LoginForm(FlaskForm):
    # Input field for the username with DataRequired validator to ensure it's not empty
    # and Length validator to specify minimum and maximum lengths
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=255)])
    # Password field for the user's password with DataRequired validator to ensure it's not empty
    password = PasswordField('Password', validators=[DataRequired()])
    # Checkbox field to enable "Remember Me" functionality for the user
    remember = BooleanField('Remember Me')
    # Submit button to initiate the login process
    submit = SubmitField('Login')

