from app import db
from app.user.models import User
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    category = db.relationship('Post', backref='post_backref', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}'')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    created_at = db.column(db.date, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    comment = db.relationship('Comment', backref='comment_backref', lazy=True)
    like = db.relationship('Like', backref='like_backref', lazy=True)
    def __repr__(self):
        return f'<Post {self.id} {self.title} >'

class Comment(db.model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    created_at = db.column(db.date, default=datetime.utcnow())

    def __repr__(self):
        return f'<Comment {self.id} {self.user_id} {self.post_id} {self.comment} >'

class Like(db.model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    status = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Comment {self.id} {self.user_id} {self.post_id} {self.status} >'
