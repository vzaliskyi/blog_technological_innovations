from flask import Blueprint
import warnings
user_bp = Blueprint('user_bp_in', __name__, template_folder="templates/user")


def create_module(app, **kwargs):
    from app.user.custom_admin import MyHomeView
    from .. import db
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
    admin = Admin(app, index_view=MyHomeView(name='Домашня'))
    from app.blog.models import Comment, Category, Post, Like
    from app.user.models import User
    from app.user.custom_admin import UserModelView, CategoryModelView, \
        PostModelView, LikeModelView, CommentModelView, CustomFileAdmin
    admin.add_view(UserModelView(User, db.session, name='Користувачі'))
    # admin.add_view(ModelView(User, db.session))
    admin.add_view(CategoryModelView(Category, db.session, name='Категорії'))
    admin.add_view(PostModelView(Post, db.session, name='Пости'))
    admin.add_view(LikeModelView(Like, db.session, name='Лайки'))
    admin.add_view(CommentModelView(Comment, db.session, name='Коментарі'))
    admin.add_view(CustomFileAdmin(app.static_folder, '/static/',
                                   name='Статичні файли'))
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset',
                                UserWarning)

from . import views  # pylint: enable=unused-import
