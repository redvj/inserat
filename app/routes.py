from flask import render_template
from app import app

# 
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Create Custem Error pages 
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    # Render the template with the 404 error status code
    return render_template('404.html'), 404