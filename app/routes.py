#---------------------------------------------------------------------------------
#------------- Imports -----------------------------------------------------------
#---------------------------------------------------------------------------------


from app import app, db
from datetime import datetime
from flask import flash, redirect, render_template, render_template,  request, url_for
from flask_login import logout_user, login_user, current_user, logout_user, login_required
from urllib.parse import urlparse
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy import or_
from app.email import send_password_reset_email
photos = UploadSet('images', IMAGES)


#------------- Forms ----------------------------------------------------------
from app.forms.login import LoginForm
from app.forms.registration import RegistrationForm
from app.forms.profileedit import ProfileEditForm
from app.forms.advertisement import AdvertisementForm, MessageForm
from app.forms.resetpasswordfrom import ResetPasswordForm, ResetPasswordRequestForm


#------------- Models ---------------------------------------------------------
from app.models.login import User
from app.models.advertisement import Advertisement, Message, Category, City, Subcategory


#---------------------------------------------------------------------------------
#------------- Home - Advertisements --------------------------------------------
#---------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
     # Get all advertisements from the database
    all_advertisements = Advertisement.query.all()
    # Get all categories from the database
    categories = Category.query.all()
     # Add this line to get all subcategories
    subcategories = Subcategory.query.all() 
    # Get all cities from the database
    cities = City.query.all()

    # Create an instance of AdvertisementForm to handle form data
    form = AdvertisementForm()

    if request.method == 'POST':
        # Get the selected category ID from the submitted form
        category_id = request.form.get('category')
        # Add this line to get the selected subcategory
        subcategory_id = request.form.get('subcategory')  
        city_id = request.form.get('city')
        # Add this line to get the minimum price
        price_min = request.form.get('price_min')
        # Add this line to get the maximum price  
        price_max = request.form.get('price_max') 

        # Initialize a list to store the filters for the advertisements
        filters = []
        if category_id:
            # Add category filter to the filters list
            filters.append(Advertisement.category_id == category_id)
        if subcategory_id:
            # Add this line to filter by subcategory
            filters.append(Advertisement.subcategory_id == subcategory_id)  
        if city_id:
            filters.append(Advertisement.city_id == city_id)
        if price_min:
            # Add this line to filter by minimum price
            filters.append(Advertisement.price >= price_min)  
        if price_max:
            # Add this line to filter by maximum price
            filters.append(Advertisement.price <= price_max)  

        # Retrieve advertisements matching the filters from the database
        filtered_advertisements = Advertisement.query.filter(*filters).all()
    else:
        # If the request method is GET, display all advertisements without filters
        filtered_advertisements = all_advertisements
    # Render the 'home.html' template with the required data
    return render_template('home.html', title='Home Page',
                           advertisements=filtered_advertisements, form=form,
                           categories=categories, subcategories=subcategories, cities=cities, all_advertisements=all_advertisements)

#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------- Create the Advertisement object (Place an ad+) --------------------
#---------------------------------------------------------------------------------
@app.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    form = AdvertisementForm()
    if form.validate_on_submit():
        # Get the uploaded image
        image = form.image.data

        if image:
            # Save the image using Flask-Uploads
            filename = photos.save(image)

            # Store the image filename in the database
            advertisement = Advertisement(
                title=form.title.data,
                description=form.description.data,
                price=form.price.data,
                contact_info=form.contact_info.data,
                city_id=form.city_id.data,
                zip_code=form.zip_code.data,
                category_id=form.category_id.data,
                subcategory_id=form.subcategory_id.data,
                user_id=form.user_id.data,
                image_filename=filename
            )
        else:
            # Handle the case when no image is uploaded
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

        # Save the advertisement to the database
        db.session.add(advertisement)
        db.session.commit()

        # Flash message and redirect
        flash('Your ad is now live!', 'success')
        return redirect(url_for('home'))

    return render_template('place_an_ad.html', title='Place an ad+', form=form)

#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- advertisements ----------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/advertisements', methods=['GET', 'POST'])
@login_required
def advertisements():
    # Retrieve all advertisements
    all_advertisements = Advertisement.query.all()
    
    # Create an instance of the AdvertisementForm
    form = AdvertisementForm()

    # Render the home.html template and pass the necessary variables
    return render_template('home.html', title='Advertisements', advertisements=all_advertisements, form=form) 


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
#------------- Dashboard - Profile page and Display and receive messages----------
#---------------------------------------------------------------------------------

@app.route('/user/<username>')
@login_required
def user(username):
    # Retrieve the user with the specified username or return a 404 error if not found
    user = User.query.filter_by(username=username).first_or_404()

    # Retrieve all advertisements associated with the user
    advertisements = Advertisement.query.filter_by(user_id=user.id).all()

    # Retrieve all messages received by the current user
    messages = Message.query.filter_by(recipient_id=current_user.id).all()

    # Render the user.html template and pass the necessary variables
    return render_template('user.html', user=user, messages=messages, 
                           advertisements=advertisements)


#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Last_seen ---------------------------------------------------------
#---------------------------------------------------------------------------------

@app.before_request
def before_request():
    # This function is executed before each request to the application

    if current_user.is_authenticated:
        # Check if the current user is authenticated

        # Get the current time in UTC format
        formatted_time = datetime.utcnow().strftime("%d-%b-%Y %H:%M:%S")

        # Convert the formatted time to a datetime object
        current_user.last_seen = datetime.strptime(formatted_time, "%d-%b-%Y %H:%M:%S")

        # Commit the changes to the database
        db.session.commit()

#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Logout ------------------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    # This route handles the logout functionality

    logout_user()
    # Use the `logout_user()` function to logout the current user

    return redirect(url_for('home'))
    # Redirect the user to the home page after logout
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Registration Form -------------------------------------------------
#---------------------------------------------------------------------------------


@app.route('/register', methods=['GET', 'POST'])
def register():
    # This route handles the registration functionality

    if current_user.is_authenticated:
        # If the user is already authenticated, redirect them to the home page
        return redirect(url_for('home'))
        

    form = RegistrationForm()
    # Create an instance of the RegistrationForm

    if form.validate_on_submit():
        # If the form is submitted and passes validation

        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
            last_name=form.last_name.data)
        # Create a new User object with the form data

        user.set_password(form.password.data)
        # Set the password for the user using the set_password() method

        db.session.add(user)
        # Add the user to the database session

        db.session.commit()
        # Commit the changes to the database

        flash('Congratulations, you are now a registered user!')
        # Display a flash message to inform the user about successful registration

        return redirect(url_for('login'))
        # Redirect the user to the login page after successful registration

    # If the form is not submitted or does not pass validation, or the route is accessed via GET

    return render_template('register.html', title='Register', form=form)
    # Render the register.html template and pass the form to the template for display



#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Edit Profil -------------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required

# This route handles the editing of the user's profile
def edit_profile():
    # Create an instance of ProfileEditForm and pass the current username to the form
    form = ProfileEditForm(current_user.username)
    
     # If the form is submitted and passes validation
    if form.validate_on_submit():
        # Update the user's profile information with the form data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Set the password for the user using the set_password() method
        current_user.set_password(form.password.data)
        
        # Commit the changes to the database
        db.session.commit()

        # Display a flash message to inform the user about successful profile update
        flash('Your profile has been updated!', 'success')
        
        # Redirect the user to their user profile page after profile update
        return redirect(url_for('user', username=current_user.username))
    
    elif request.method == 'GET':
        # If the route is accessed via GET, pre-populate the form with the user's current profile information
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Render the edit_profile.html template and pass the form to the template for display
    return render_template('edit_profile.html', title='Edit Profile', form=form)


#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Delete_profile ----------------------------------------------------
#---------------------------------------------------------------------------------

# This route handles the deletion of the user's profile
@app.route('/delete_profile', methods=['POST'])
def delete_profile():


    # Get the current user
    user = current_user

    # If the user is an admin, display a flash message and redirect them to their user profile page
    if user.is_admin:
        flash('Admin account can not be be deleted')
        return redirect(url_for('user', username=current_user.username))
    
    # If the user is not an admin
    else:
        
        
        # Delete the user from the database and commit the changes
        db.session.delete(user)
        db.session.commit()

        # Display a flash message to inform the user about successful account deletion
        flash('Your account has been successfully deleted')
    
    # Redirect the user to the home page after account deletion
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

# This route handles the password reset request functionality
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():

    if current_user.is_authenticated:
        # If the user is already authenticated, redirect them to the home page
        return redirect(url_for('home'))
    
    # Create an instance of ResetPasswordRequestForm to handle form data
    form = ResetPasswordRequestForm()
    
    # If the form is submitted and passes validation
    if form.validate_on_submit():

        # Find the user based on the provided email
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # If a user with the provided email is found, send a password reset email
            send_password_reset_email(user)
        # Display a flash message to inform the user about password reset instructions
        flash('Check your email for the instructions to reset your password')
        
        # Redirect the user to the login page after sending the password reset email
        return redirect(url_for('login'))
    
    # Render the reset_password_request.html template and pass the form to the template for display
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
 
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
#------------- Send-Message in advertisement  (Receiving is with Dashbaord) ------
#---------------------------------------------------------------------------------

# This route handles sending a message to the user who posted the specified advertisement
@app.route('/send_message/<int:advertisement_id>', methods=['GET', 'POST'])
@login_required
def send_message(advertisement_id):

    # Get the advertisement with the given advertisement_id, or return a 404 error if not found
    advertisement = Advertisement.query.get_or_404(advertisement_id)
    
    # If the request method is POST (i.e., the message form is submitted)
    if request.method == 'POST':

        # Get the content of the message from the form data
        content = request.form['message_content']
        # Get the ID of the user who posted the advertisement to send the message to
        recipient_id = advertisement.user.id
        
        # Create a new message and add it to the database
        message = Message(sender=current_user, recipient_id=recipient_id, content=content)
        db.session.add(message)
        db.session.commit()

        # Display a flash message to inform the user about successful message sending
        flash('Message deleted successfully.', 'success')

        # Redirect the user to the home page
        return redirect(url_for('home'))
    
    # If the request method is not POST (i.e., accessing the route via GET)
    # Render the send_message.html template and pass the advertisement to the template for display
    return render_template('send_message.html', advertisement=advertisement)


#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Deleting a message ( in Dashbaord) --------------------------------
#---------------------------------------------------------------------------------

# This route handles deleting a specific message
@app.route('/delete_message/<message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    
    # Get the message with the given message_id, or return a 404 error if not found
    message = Message.query.get_or_404(message_id)
    
    if message.recipient_id != current_user.id:
        # If the recipient of the message is not the current user, they are not authorized to delete it
        flash('You are not authorized to delete this message.', 'danger')
        # Redirect the user to their user profile page
        return redirect(url_for('user'))
        
    # Delete the message from the database#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Deleting a message ( in Dashbaord) --------------------------------
#---------------------------------------------------------------------------------
    db.session.delete(message)
    db.session.commit()

    # Display a flash message to inform the user about successful message deletion
    flash('Message was sent.', 'success')

    # Redirect the user to their user profile page
    return redirect(url_for('user', username=current_user.username))

#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------- Sending a reply to a message ( in Dashbaord) ----------------------
#---------------------------------------------------------------------------------

# This route handles sending a reply to a specific message
@app.route('/send_reply/<int:message_id>', methods=['POST'])
@login_required
def send_reply(message_id):

    # Get the message with the given message_id, or return a 404 error if not found
    message = Message.query.get_or_404(message_id)
    
    if message.recipient_id != current_user.id:
        # If the recipient of the message is not the current user, they are not authorized to reply
        flash('You are not authorized to reply to this message.', 'danger')
        return redirect(url_for('messages'))
    #---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Deleting a message ( in Dashbaord)#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Deleting a message ( in Dashbaord) --------------------------------
#--------------------------------------------------------------------------------- --------------------------------
#---------------------------------------------------------------------------------
    # If the request method is POST (i.e., the reply form is submitted)
    if request.method == 'POST':

        # Get the content of the reply from the form data
        reply_content = request.form['reply_content']

        # Get the ID of the original sender of the message to send the reply to
        recipient_id = message.sender_id
        
        # Create a new message as the reply and add it to the database
        reply_message = Message(sender_id=current_user.id, recipient_id=recipient_id, content=reply_content)
        db.session.add(reply_message)
        db.session.commit()
        
        # Display a flash message to inform the user about successful reply sending
        flash('Reply sent successfully.', 'success')

        # Redirect the user to their user profile page
        return redirect(url_for('user', username=current_user.username))
    
    # Redirect the user to their user profile page
    return redirect(url_for('user', username=current_user.username))

#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Deleting Advertisements  ( in Dashbaord) --------------------------------
#---------------------------------------------------------------------------------

@app.route('/delete_ad/<int:ad_id>', methods=['POST'])
def delete_ad(ad_id):
    # Assuming you have an Advertisement model
    ad = Advertisement.query.get(ad_id)

    if ad:
        # Delete the advertisement from the database
        db.session.delete(ad)
        db.session.commit()
        flash('Advertisement deleted successfully.', 'success')
    else:
        flash('Advertisement not found.', 'error')

    # Redirect the user to their user profile page
    return redirect(url_for('user', username=current_user.username))

#---------------------------------------------------------------------------------

