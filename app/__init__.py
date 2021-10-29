from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from .blog import blog_bp
from .user import user_bp
app.register_blueprint(blog_bp, url_prefix='')
app.register_blueprint(user_bp, url_prefix='auth')

from app import view