#---------------------------------------------------------------------------------
#------------- Imports -----------------------------------------------------------
#---------------------------------------------------------------------------------

from flask import flash, redirect, render_template, render_template,  request, url_for
from app import app, db
from datetime import datetime
from werkzeug.urls import url_parse
from flask_login import logout_user
from flask_login import login_required
from flask_login import login_user, current_user, logout_user
from urllib.parse import urlparse

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

#------------- Forms ----------------------------------------------------------
from app.forms.login import LoginForm
from app.forms.registration import RegistrationForm
from app.forms.profileedit import ProfileEditForm
from app.forms.advertisement import AdvertisementForm
from app.forms.contact import ContactForm
from app.forms.message import MessageForm

from app.forms.resetpasswordfrom import ResetPasswordForm, ResetPasswordRequestForm


#------------- Models ---------------------------------------------------------
from app.models.login import User
from app.models.advertisement import Advertisement
from app.models.advertisement import Category
from app.models.contact import Contact
from app.models.message import Message

from app.email import send_password_reset_email



#---------------------------------------------------------------------------------
#------------- Startpage ---------------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'] )
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    all_advertisements = Advertisement.query.all()
    form = AdvertisementForm()
    return render_template('home.html',  advertisements=all_advertisements, form=form)


#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Place an ad+ -------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    form = AdvertisementForm()
    if form.validate_on_submit():
        advertisement = Advertisement(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            contact_info=form.contact_info.data,
            city_id=form.city_id.data,
            zip_code=form.zip_code.data,
            category_id=form.category_id.data,
            subcategory_id=form.subcategory_id.data,
            user_id=form.user_id.data
        )
        db.session.add(advertisement)
        db.session.commit()
        flash('Your ad is now live!')
        return redirect(url_for('start'))
    return render_template('place_an_ad.html', title='Place an ad', form=form)

#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
#------------- Create Custem Error pages -----------------------------------------
#---------------------------------------------------------------------------------

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    # Render the template with the 404 error status code
    return render_template('404.html'), 404 


# Custom 500 error page
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------- User Login --------------------------------------------------------
#---------------------------------------------------------------------------------

# Login URL
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from urllib.parse import urlparse
# Import the necessary modules and classes


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # If the user blocked - Admin Panel
        if user and user.is_blocked:
            flash('You have been locked by the administrator')
            return redirect(url_for('login'))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            # If the user is admin - Admin Panel
            if user.is_admin:
                return redirect(url_for('user', username=current_user.username))
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)



#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------- Profile page --------------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}

    ]

   
  
    return render_template('user.html', title='Dashboard', user=user, posts=posts)


#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Last_seen ---------------------------------------------------------
#---------------------------------------------------------------------------------

@app.before_request
def before_request():
    if current_user.is_authenticated:
        formatted_time = datetime.utcnow().strftime("%d-%b-%Y %H:%M:%S")
        current_user.last_seen = datetime.strptime(formatted_time, "%d-%b-%Y %H:%M:%S")
        db.session.commit()


#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Logout ------------------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------- Template --------------------------------------------------------...
#---------------------------------------------------------------------------------




#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Registration Form -------------------------------------------------
#---------------------------------------------------------------------------------


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Route /register wurde mit POST betreten. Prüfung, ob alles o.k. ist:
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
            last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    # Route /register wurde mit GET betreten
    return render_template('register.html', title='Register', form=form)



#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Edit Profil -------------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm(current_user.username)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)


#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Delete_profile ----------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    # Get the current user
    user = current_user

    if user.is_admin:
        flash('Admin account can not be be deleted')
        return redirect(url_for('user', username=current_user.username))
    else:
        
        # Delete the user and commit the changes
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been successfully deleted')
        # Redirect the user to a relevant page (e.g., home page or login page)
    return redirect(url_for('home'))

#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------- Admin Panel -------------------------------------------------------
#---------------------------------------------------------------------------------

from flask import abort
@app.route('/admin')
def admin_Panel():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)  # Return a forbidden error if the user is not an admin
      
    else:
        # Render the admin page for admin users
    
       return render_template('admin/index.html')
    
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Password-recovery/reset -------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    # Rest of your code
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Password-recovery/reset -------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/contact/<int:user_id>', methods=['GET', 'POST'])
def contact_user(user_id):
    advertisements = Advertisement.query.all()  # Retrieve the advertisements from the database
    form = MessageForm(advertisements=advertisements)
    user = User.query.get(user_id)
    if not user:
        return 'User not found'

    form = MessageForm()
    if form.validate_on_submit():
        content = form.content.data
        message = Message(content=content, sender_id=current_user.id, recipient_id=user_id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('contact_user', user_id=user_id))

    return render_template('contact.html', user=user, form=form)

#---------------------------------------------------------------------------------


@app.route('/message_board/<int:user_id>')
def message_board(user_id):
    user = User.query.get(user_id)
    return render_template('message_board.html', title='Message Board', user=user)

