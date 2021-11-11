from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
mail = Mail(app)

from .blog import blog_bp  # linting: disable=E402
from .user import user_bp  # linting: disable=E402
app.register_blueprint(blog_bp, url_prefix='')
app.register_blueprint(user_bp, url_prefix='/auth')

from app import views  # linting: disable=unused-import
from app import forms  # linting: disable=unused-import
