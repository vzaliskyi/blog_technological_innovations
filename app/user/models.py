from app import db, bcrypt
from app.blog.models import Post, Category, Comment, Like
from flask_login import UserMixin


class User(db.Model):

    def __init__(self, username, email, password, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    picture = db.Column(db.String(20), nullable=False, server_default='default.jpg')

    comment = db.relationship('Comment', backref='user_br', lazy=True)
    like = db.relationship('Like', backref='user_br', lazy=True)
    posts = db.relationship('Post', backref='user_br', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
