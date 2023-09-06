from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_moment import Moment
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail


# Create the Flask application instance
app = Flask(__name__)

# Load the configuration from the Config class in config.py
app.config.from_object(Config)

# Initialize the SQLAlchemy database object
db = SQLAlchemy(app)

# Initialize the Flask-Migrate extension for database migrations
Migrate(app, db)

# Initialize the Flask-Login extension for user authentication
login = LoginManager(app)
login.login_view = 'login'

# Initialize the Flask-Mail extension for sending emails
mail = Mail(app)

# Initialize the Flask-Moment extension for date and time formatting
moment = Moment(app)

# Configure the Flask-Uploads extension for file uploads
photos = UploadSet('images', IMAGES)
configure_uploads(app, photos)

# Import the application routes and models
from app import routes, api
from app.models import controlpanel, advertisement