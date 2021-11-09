from app import app
# from .user import view
from flask import render_template


@app.route('/')
def home():
    return render_template('home.html', title='Home page')
