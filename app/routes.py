from flask import render_template, url_for, flash, redirect, request
from app import app
from app.forms.login import LoginForm
from app.forms.job import JobForm
from werkzeug.urls import url_parse
from app.models.login import User
from flask_login import logout_user
from flask_login import login_required

from flask_login import login_user, current_user

#---------------------------------------------------------------------------------
#------------- Startpage -----------------------------------------
#---------------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    return render_template('home.html', titel='Home')

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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Log the user in and redirect to the homepage
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    # Display the login form
    return render_template('login.html', title='Sign In', form=form)


#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Logout --------------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------- Create_Job --------------------------------------------------------
#---------------------------------------------------------------------------------

@app.route('/create_job', methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            description=form.description.data,
            requirements=form.requirements.data,
            location=form.location.data
        )
        db.session.add(job)
        db.session.commit()
        flash('Job created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_job.html', form=form)


#---------------------------------------------------------------------------------
