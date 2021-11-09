from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=3, max=20, message="Username повинен бути від 3 до 20 символів")])
    # email = StringField('Email', validators=[DataRequired(), Email(message="Невірно введений email!")])

    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, message="Пароль повинен містити від 8 символів")])

    confirm_password = PasswordField('Підтвердіть пароль',
        validators=[DataRequired(), EqualTo('password', message="Паролі не співпадають")])

    submit = SubmitField("Зареєструватися")

    def validate_username(self, username):
        user = User.query.filter_by(user_login=username.data).first()
        if user:
            raise ValidationError('Такий юзернейм вже існує, виберіть інший')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Пароль', validators=[DataRequired()])

    submit = SubmitField("Вхід")