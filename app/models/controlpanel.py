
# -- Flask-Admin ---------------------------------------------------------------------
# https://flask-admin.readthedocs.io/en/latest/introduction/#authorization-permissions


from flask import Flask
from sqlalchemy import func

from flask import redirect, url_for, request

from flask_login import current_user
from werkzeug.exceptions import HTTPException

from app import db, app, login
from app.models.login import User
from app.models.advertisement import Category, Subcategory, Advertisement, City, Message

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers as admin_helpers


# Create User - ModelView
class UserView(ModelView):
    column_list = ['id', 'first_name', 'last_name', 'username', 'email','user_adedd', 'last_seen', 'is_admin', 'is_blocked']
    form_columns = ['first_name', 'last_name', 'username', 'email', 'password_hash', 'is_admin',  'is_blocked']
    column_searchable_list = ['username', 'email', 'last_name']
    
    # Flask Admin is displayed as a password field to ensure that the user's 
    # input is protected and the characters entered are not visible.
    form_widget_args = {
        'password_hash': {
            'type': 'password'
        }
    }

    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
    


# Category and Sub* db - ModelView
class CategoryModelView(ModelView):
    column_display_pk = True  # Display the primary key in the list view
    form_columns = ('name', 'subcategories')  # Specify the columns to include in the form

class SubcategoryModelView(ModelView):
    column_display_pk = True
    form_columns = ('name', 'category')

# Advertisement* db - ModelView
class AdvertisementModelView(ModelView):
    column_display_pk = True
    form_columns = ('title', 'description', 'category', 'subcategory', 'city', 'price', 'user', 'zip_code', 'timestamp', 'images')


class CityModelView(ModelView):
    column_display_pk = True
    form_columns = ('name', )


# Send and Receiving* db - ModelView
class ReceivedMessageModelView(ModelView):
    column_display_pk = True
    form_columns = ('content','sender','recipient_id' )
    column_list = ['id', 'sender', 'content', 'timestamp']







admin = Admin(app, name='Admin Panel', template_mode='bootstrap4') 

# adds a view for the user model to the Flask admin interface. 
# This view allows you to view, edit, and delete records of the user model in Admin Panel (/admin)
admin.add_view(UserView(User, db.session))
admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(SubcategoryModelView(Subcategory, db.session))
admin.add_view(AdvertisementModelView(Advertisement, db.session))
admin.add_view(CityModelView(City, db.session))

admin.add_view(ReceivedMessageModelView(Message, db.session))

@app.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
