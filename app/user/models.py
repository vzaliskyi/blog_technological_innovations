from app.blog.models import Comment, Like, Post
from app import db, bcrypt, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # type: ignore

    def __init__(self, username, email, password, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    username = db.Column(db.String(30), unique=True, nullable=False)
    # type: ignore
    email = db.Column(db.String(50), unique=True, nullable=False)
    # type: ignore
    password = db.Column(db.String(30), nullable=False)
    # type: ignore
    picture = db.Column(db.String(20), nullable=False,
                        server_default='default.jpg')  # type: ignore

    comment = db.relationship('Comment', backref='user_br', lazy=True)
    # type: ignore
    like = db.relationship('Like', backref='user_br', lazy=True)
    # type: ignore
    posts = db.relationship('Post', backref='user_br', lazy=True)

    # type: ignore

    def verify_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

    def get_reset_token(self, expires_sec=900):
        s_obj = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s_obj.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s_obj = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s_obj.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # #/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/
    # методи для опрацювання ставлення лайків/дизлайків на пост
    def like_post(self, post):
        print('like_post')
        if not self.is_rated_post(post):
            like = Like(user_id=self.id, post_id=post.id, status=True)
            db.session.add(like)
            print('like_post +')

    def dislike_post(self, post):
        print('dislike_post')
        if not self.is_rated_post(post):
            like = Like(user_id=self.id, post_id=post.id, status=False)
            db.session.add(like)
            print('dislike_post +')

    def change_rate(self, post):
        print('change_rate')
        rate = Like.query.filter_by(user_id=self.id, post_id=post.id).first()
        if rate.status:
            print('change_rate False')
            rate.status = False
        else:
            print('change_rate True')
            rate.status = True

    def unrate_post(self, post):
        print('unrate_post')
        if self.is_rated_post(post):
            Like.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    # чи ставив користувач лайки/дизлайки
    def get_rate_status(self, post):
        print('get_rate_status')
        rate = Like.query.filter(
            Like.user_id == self.id,
            Like.post_id == post.id).first().status
        return rate

    def get_rate_status666(self, post):
        print('get_rate_status666')
        if self.is_rated_post(post):
            rate = Like.query.filter(
                Like.user_id == self.id,
                Like.post_id == post.id).first().status
            return rate
        else:
            return None

    def is_rated_post(self, post):
        print('is_rated_post')
        return Like.query.filter(
            Like.user_id == self.id,
            Like.post_id == post.id).count() > 0

    #
    # def is_rated_post(self, post):
    #     rate = Like.query.filter(
    #         Like.user_id == self.id,
    #         Like.post_id == post.id)
    #     if rate.count() == 0:
    #         return False, None
    #     elif rate.count() == 1:
    #         return True, rate.status

    # def unlike_post(self, post):
    #     self.unrate_post(post)
    #
    # def undislike_post(self, post):
    #     self.unrate_post(post)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
