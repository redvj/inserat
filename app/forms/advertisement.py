from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField, ValidationError
from wtforms.validators import DataRequired
from app.models.advertisement import Category, Subcategory, City
from app.models.login import User
from flask_login import current_user
from flask_wtf.file import FileAllowed

# Form for creating/editing a category
class CategoryForm(FlaskForm):
     # Input field for the name of the category
    name = StringField('Name', validators=[DataRequired()])

# Form for creating/editing a subcategory
class SubcategoryForm(FlaskForm):
    # Input field for the name of the subcategory
    name = StringField('Name', validators=[DataRequired()])
    # Dropdown field to select the parent category of the subcategory
    category_id = SelectField('Category', coerce=int)

# Form for creating/editing an advertisement
class AdvertisementForm(FlaskForm):
    # Input field for the title of the advertisement
    title = StringField('Title', validators=[DataRequired()])
    # field for the description of the advertisement
    description = TextAreaField('Description', validators=[DataRequired()])
    # Input field for the price of the advertisement
    price = StringField('Price', validators=[DataRequired()])
    # Input field for the contact information for the advertisement
    contact_info = StringField('Contact Information')
    # Input field for the ZIP code of the advertisement
    zip_code = StringField('ZIP Code', validators=[DataRequired()] )
    
    # Dropdown field to select the category, subcategory, city, user of the advertisement
    category_id = SelectField('Category')
    subcategory_id = SelectField('Subcategory')
    city_id = SelectField('City')
    user_id = SelectField('User', coerce=int)

    # File field for uploading an image associated with the advertisement
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    


    # Custom constructor to populate the choices for some SelectFields
    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
        
        # Set the choices for the category_id field using the categories retrieved from the database
        self.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
        self.subcategory_id.choices = [(subcategory.id, subcategory.name) for subcategory in Subcategory.query.all()]
        self.user_id.choices = [(current_user.id, current_user.username)]
        self.city_id.choices = [(city.id, city.name) for city in City.query.all()]


# Form for sending a message
class MessageForm(FlaskForm):
    # Field for the content of the message
    content = TextAreaField('Content', validators=[DataRequired()])
    # Submit button to send the message
    submit = SubmitField('Send')