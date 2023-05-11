


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class JobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    company = StringField('Company', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    requirements = TextAreaField('Requirements', validators=[DataRequired(), Length(max=1000)])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])


