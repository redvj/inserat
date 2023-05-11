from flask import render_template, url_for, flash, redirect
from app import app
from app.forms.login import LoginForm
from app.forms.job import JobForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    user = {'username': 'Vijay', 'username': 'Adi'}
    
    posts = [
        {
            'author': {'username': 'Vijay'},
            'body': 'Die Anmeldung scheint zu klappen!'
        }
    ]
  


    return render_template('home.html', titel='Home', user=user, posts=posts,)



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
    # create a LoginForm instance
    form = LoginForm()

    # handle form submission
    if form.validate_on_submit():
        # submitted form data
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember.data))
        return redirect('/home')

    # render the login form
    return render_template('login.html', title='Login', form=form)

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
