from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime

class Inserat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    category = db.Column(db.String(255), nullable=False)