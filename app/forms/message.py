from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


#Übernommen aus den Beispielen Microblog
class MessageForm(FlaskForm):
    advertisement_id = SelectField('Advertisement ID', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')