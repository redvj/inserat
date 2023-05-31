from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app.models.advertisement import Category, Subcategory
from app.models.login import User
from flask_login import current_user

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

class SubcategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)

class AdvertisementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category_id = SelectField('Category')
    subcategory_id = SelectField('Subcategory')
    user_id = SelectField('User', coerce=int)
    
    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
        self.subcategory_id.choices = [(subcategory.id, subcategory.name) for subcategory in Subcategory.query.all()]
        self.user_id.choices = [(current_user.id, current_user.username)]

