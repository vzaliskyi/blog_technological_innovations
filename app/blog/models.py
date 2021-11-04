from app import db
# from app.user.models import User
from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)

    category = db.relationship('Post', backref='category_br', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}'')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.Date, default=datetime.utcnow())

    comments = db.relationship('Comment', backref='post_br', lazy=True)
    likes = db.relationship('Like', backref='post_br', lazy=True)

    def __repr__(self):
        return f'<Post {self.id} {self.title} >'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id} {self.user_id} {self.post_id} ' \
               f'{self.text} >'


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    status = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Like {self.id} {self.user_id} {self.post_id} ' \
               f'{self.status} >'
