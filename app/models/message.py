from app import db, app, login
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    advertisement_id = db.Column(db.Integer, db.ForeignKey('advertisement.id'), nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='messages_sent')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='messages_received')
    advertisement = db.relationship('Advertisement', backref='messages')

    def __repr__(self):
        return f'<Message {self.id}>'