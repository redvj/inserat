# Import necessary modules and objects
from datetime import datetime, timedelta
from app import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import os
import jwt
from time import time

#Übernommen aus den Beispielen Microblog

# Method for Avatare
from hashlib import md5


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_adedd = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)  # registered users can be blocked from logging in
    advertisements = db.relationship('Advertisement', backref='user', lazy=True)
    
    
    # Method to set a user's password (hashing the password)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # Method to check if a provided password matches the user's hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Representation method to show the user's username when printing an instance of User
    def __repr__(self):
        return '<User {}>'.format(self.username)
    # Method to generate a user's avatar using Gravatar
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size
            )
    # Method to generate a reset password token
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    # Static method to verify a reset password token
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
# This function is used by Flask-Login to load the user object from the user ID stored in the session
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

