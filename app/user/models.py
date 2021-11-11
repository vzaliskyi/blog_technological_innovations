from app.blog.models import Comment, Like, Post
from app import db, bcrypt, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    def __init__(self, username, email, password, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    picture = db.Column(db.String(20), nullable=False,
                        server_default='default.jpg')

    comment = db.relationship('Comment', backref='user_br', lazy=True)
    like = db.relationship('Like', backref='user_br', lazy=True)
    posts = db.relationship('Post', backref='user_br', lazy=True)

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

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
