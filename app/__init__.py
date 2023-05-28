from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager

# For Admin Panel
from flask_admin.contrib.sqla import ModelView

# For Mail Recovery
from flask_mail import Mail


app = Flask(__name__)

# Load the config.py file
app.config.from_object(Config)
db = SQLAlchemy(app)
Migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

if __name__ == '__main__':
    app.run(debug=True)


from app import routes
from app.models import login, controlpanel