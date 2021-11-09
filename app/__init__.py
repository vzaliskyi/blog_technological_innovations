from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)


from .blog import blog_bp  # pylint: disable=import-error
from .user import user_bp  # pylint: disable=import-error
app.register_blueprint(blog_bp, url_prefix='')
app.register_blueprint(user_bp, url_prefix='/auth')

from app import views
from app import forms

