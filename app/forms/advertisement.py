from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField,FloatField,IntegerField
from wtforms.validators import DataRequired
from app.models.advertisement import Category, Subcategory, City
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
    price = FloatField('Price')
    contact_info = StringField('Contact Information')

    city_id = SelectField('City', validators=[DataRequired() ])
    zip_code = IntegerField('ZIP Code', validators=[DataRequired()])

    category_id = SelectField('Category', validators=[DataRequired()], coerce=int)
    subcategory_id = SelectField('Subcategory', coerce=int)
    user_id = SelectField('User', validators=[DataRequired()])

    # The code retrieves all objects from the database
    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
        self.subcategory_id.choices = [(subcategory.id, subcategory.name) for subcategory in Subcategory.query.all()]
        self.user_id.choices = [(current_user.id, current_user.username)]
        self.city_id.choices = [(city.id, city.name) for city in City.query.all()]
