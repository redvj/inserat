from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models.login import User


class ProfileEditForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Profile')

    def __init__(self, current_user, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.current_user = current_user


    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user and user.id != self.current_user.id:
            raise ValidationError('Username already taken. Please choose a different username.')