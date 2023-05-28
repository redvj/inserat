from app import app
from app.models.login import User

if __name__ == '__main__':
    app.run(debug=True)