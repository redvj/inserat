import os

# Get the absolute path of the directory containing the current file
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# This class defines the configuration options for the application
class Config:
    
    # The secret key used for session encryption. If not provided as an environment variable, a default value is used
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    
    # The URI for the database. 
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #   'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Neu:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Disable modification tracking for SQLAlchemy to improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    # Configuration options for sending emails using Gmail SMTP. The values are obtained from environment variables

    # Configuration for Flask-Uploads
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'app/static')
    # The destination directory for uploaded photos

    # Additional configuration options
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    # The maximum allowed content length for uploaded files

    UPLOADS_DEFAULT_DEST = 'app/static'
    # The default destination directory for uploaded files

    UPLOADED_PHOTOS_ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')
    # The allowed file extensions for uploaded photos

    #UPLOADED_PHOTOS_ALLOWED_MIMETYPES = ('image/jpeg', 'image/png', 'image/gif')
    # The allowed MIME types for uploaded photos

