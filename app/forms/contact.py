from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Form for sending a contact message
class ContactForm(FlaskForm):
    # Textarea field for the content of the message with DataRequired validator to ensure it's not empty
    message = TextAreaField('Message', validators=[DataRequired()])
    # Submit button to send the message
    submit = SubmitField('Send')