from app import db
# from app.user.models import User
from datetime import datetime


class Category(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    name = db.Column(db.String(25), unique=True, nullable=False)
    # type: ignore

    category = db.relationship('Post', backref='category_br', lazy=True)

    # type: ignore

    def __repr__(self):
        return f"Category('{self.name}'')"


class Post(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)  # type: ignore
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))  # type: ignore
    title = db.Column(db.String(100), nullable=False)  # type: ignore
    content = db.Column(db.Text)  # type: ignore
    created_at = db.Column(db.Date, default=datetime.utcnow())  # type: ignore

    comments = db.relationship('Comment', backref='post_br', lazy=True)
    # type: ignore
    likes = db.relationship('Like', backref='post_br', lazy=True)

    # type: ignore

    def total_likes(self):
        return Like.query.filter(
            Like.post_id == self.id,
            Like.status == True).count()

    def total_dislikes(self):
        return Like.query.filter(
            Like.post_id == self.id,
            Like.status == False).count()

    def __repr__(self):
        return f'<Post {self.id} {self.title} >'


class Comment(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # type: ignore
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # type: ignore
    text = db.Column(db.String(500), nullable=False)  # type: ignore
    created_at = db.Column(db.Date, default=datetime.utcnow)  # type: ignore

    def __repr__(self):
        return f'<Comment {self.id} {self.user_id} {self.post_id} ' \
               f'{self.text} >'


class Like(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # type: ignore
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # type: ignore
    status = db.Column(db.Boolean)  # type: ignore

    def __repr__(self):
        return f'<Like {self.id} {self.user_id} {self.post_id} ' \
               f'{self.status} >'
