from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models.login import User

#Übernommen aus den Beispielen Microblog

# Form for editing user profile information
class ProfileEditForm(FlaskForm):

     # Input field for the first name, last name,username,email, current password with DataRequired validator
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Password field for confirming the new password with DataRequired and EqualTo('password') validators
    # to ensure that the password is repeated correctly
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Submit button to save the changes to the user's profile
    submit = SubmitField('Update Profile')

    # Store the original username to check if it is changed during validation
    def __init__(self, original_username, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    # Custom validation method for the username field
    def validate_username(self, username):
         # If the username is being changed
        if username.data != self.original_username:
            # Check if the new username already exists in the database
            user = User.query.filter_by(username=self.username.data).first()
            # If the username already exists, raise a ValidationError
            if user is not None:
                raise ValidationError('Please use a different username.')