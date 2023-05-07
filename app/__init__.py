from flask import Flask
from config import Config

app = Flask(__name__)

# Load the config.py file
app.config.from_object(Config)



if __name__ == '__main__':
    app.run(debug=True)


from app import routes