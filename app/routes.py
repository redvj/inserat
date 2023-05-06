from flask import render_template, request
from app import app

@app.route('/')
@app.route('/home')
def home():
    return "<h1>Hello, Flask!!</h1>"