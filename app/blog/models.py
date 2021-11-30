from app import db, search
# from app.user.models import User
from datetime import datetime
# from flask_sqlalchemy import hybrid_property
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


class Category(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    name = db.Column(db.String(25), unique=True, nullable=False)
    # type: ignore

    category = db.relationship('Post', backref='category_br', lazy=True)

    # type: ignore

    def __repr__(self):
        return f"Category('{self.name}'')"


class Post(db.Model):  # type: ignore
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)  # type: ignore
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))  # type: ignore
    title = db.Column(db.String(100), nullable=False)  # type: ignore
    content = db.Column(db.Text)  # type: ignore
    created_at = db.Column(db.DateTime, default=datetime.now)  # type: ignore

    comments = db.relationship('Comment', backref='post_br', lazy=True)
    # type: ignore
    likes = db.relationship('Like', backref='post_br', lazy=True)

    # type: ignore

    def total_posts_by_category(self, category_id):
        return Post.query.filter(Post.category_id == category_id).count()

    def total_posts_by_user(self, user_id):
        return Post.query.filter(Post.user_id == user_id).count()

    def total_comments(self):
        return Comment.query.filter(Comment.post_id == self.id).count()

    def total_likes(self):
        return Like.query.filter(
            Like.post_id == self.id,
            Like.status == True).count()

    def total_dislikes(self):
        return Like.query.filter(
            Like.post_id == self.id,
            Like.status == False).count()

    def get_like_percentage(self):
        num_of_rates = self.total_likes() + self.total_dislikes()
        # print('get_like_percentage')
        if num_of_rates == 0:
            return 50
        else:
            return int(self.total_likes() / num_of_rates * 100)

    # @hybrid_property
    # def rate_difference(self):
    #     total_l = Like.query.filter(
    #         Like.post_id == self.id,
    #         Like.status == True).count()
    #     total_d = Like.query.filter(
    #         Like.post_id == self.id,
    #         Like.status == False).count()
    #
    #     num_of_rates = total_l + total_d
    #     return num_of_rates

    def __repr__(self):
        return f'<Post {self.id} {self.title} >'


class Comment(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # type: ignore
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # type: ignore
    text = db.Column(db.String(500), nullable=False)  # type: ignore
    created_at = db.Column(db.DateTime, default=datetime.now)  # type: ignore

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


# створюємо індекси для пошуку по таблиці Post
# search.create_index(Post)
