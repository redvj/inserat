
# -- Flask-Admin ---------------------------------------------------------------------
# https://flask-admin.readthedocs.io/en/latest/introduction/#authorization-permissions


from flask import Flask
from flask import redirect, url_for, request

from flask_login import current_user
from werkzeug.exceptions import HTTPException

from app import db, app, login
from app.models.login import User

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers as admin_helpers



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
    


    

admin = Admin(app, name='Admin Panel', template_mode='bootstrap4') 

# adds a view for the user model to the Flask admin interface. 
# This view allows you to view, edit, and delete records of the user model.
admin.add_view(UserView(User, db.session))

@app.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
