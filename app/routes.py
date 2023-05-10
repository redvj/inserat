from flask import render_template, url_for, flash, redirect
from app import app
from app.forms.login import LoginForm


@app.route('/')
@app.route('/home')
def home():
  
    return render_template('home.html')



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
    form = LoginForm()
    if form.validate_on_submit():
        
        flash('Login erfolgreich.', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

#---------------------------------------------------------------------------------