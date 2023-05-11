from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Load the config.py file
app.config.from_object(Config)
db = SQLAlchemy(app)
Migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)


from app import routes