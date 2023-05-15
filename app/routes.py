from flask import render_template, url_for, flash, redirect, request
from app import app, db

from app.forms.login import LoginForm
from app.forms.registration import RegistrationForm

from app.models.login import User


from werkzeug.urls import url_parse
from flask_login import logout_user
from flask_login import login_required
from flask_login import login_user, current_user



#---------------------------------------------------------------------------------
#------------- Startpage -----------------------------------------
#---------------------------------------------------------------------------------

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    posts = [
        {
            'author': {'username': 'Vijay'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('home.html', titel='Home', posts=posts)

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
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Log the user in and redirect to the homepage
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    # Display the login form
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


    return render_template('user.html', user=user, posts=posts)


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
#------------- ******* --------------------------------------------------------
#---------------------------------------------------------------------------------




#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------- Registration Form --------------------------------------------------------
#---------------------------------------------------------------------------------


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



#---------------------------------------------------------------------------------
