from app import db, app, login
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Model class for the 'categories' table
class Category(db.Model):
    # Primary key column for the category
    id = db.Column(db.Integer, primary_key=True)
    # Column for the category name, unique and not nullable
    name = db.Column(db.String(50), unique=True, nullable=False)
    # Relationship definition to associate Category with Subcategory through the 'subcategories' attribute
    subcategories = db.relationship('Subcategory', back_populates='category', lazy=True)
    # Representation method to show the category name when printing an instance of Category
    def __repr__(self):
        return f'<Category {self.name}>'

# Model class for the 'subcategories' table
class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='subcategories')

    def __repr__(self):
        return f'<Subcategory {self.name}>'

# Model class for the 'cities' table
class City(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<City {self.name}>'

# Model class for the 'advertisements' table
class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float)
    contact_info = db.Column(db.String(255))

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False, index=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Add this line for the image filename
    image_filename = db.Column(db.String(100)) 
   
    # Relationship definitions
    city = db.relationship('City', backref='advertisements')
    category = db.relationship('Category', backref='advertisements')
    subcategory = db.relationship('Subcategory', backref='advertisements')
    images = db.relationship('AdvertisementImage', backref='advertisement', lazy=True)


    def __repr__(self):
        return f'<Advertisement {self.title}>'

# Model class for the 'messages' table
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender = db.relationship('User', backref='sent_messages', foreign_keys=[sender_id])
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
# Model class for the 'advertisement_images' table
class AdvertisementImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    advertisement_id = db.Column(db.Integer, db.ForeignKey('advertisement.id'), nullable=False)