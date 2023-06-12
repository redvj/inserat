from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField, ValidationError
from wtforms.validators import DataRequired
from app.models.advertisement import Category, Subcategory, City
from app.models.login import User
from flask_login import current_user
from flask_wtf.file import FileAllowed

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

class SubcategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)

class AdvertisementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    contact_info = StringField('Contact Information')
    zip_code = StringField('ZIP Code', validators=[DataRequired()] )
    
    category_id = SelectField('Category')
    subcategory_id = SelectField('Subcategory')
    city_id = SelectField('City')
    user_id = SelectField('User', coerce=int)
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    


    
    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
        self.subcategory_id.choices = [(subcategory.id, subcategory.name) for subcategory in Subcategory.query.all()]
        self.user_id.choices = [(current_user.id, current_user.username)]
        self.city_id.choices = [(city.id, city.name) for city in City.query.all()]



class MessageForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')