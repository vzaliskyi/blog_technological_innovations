from .models import User
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Regexp, Length, EqualTo, \
    ValidationError
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(message='Заповніть це поле!'), Email(message='Некоректна email адреса!')]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired(message='Заповніть це поле!')]
    )
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField('Увійти')


class RegistrationForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[Length(min=3, max=30,
                           message='Поле повинно бути довжиною від 3 до 30 симолів!'),
                    DataRequired(message='Заповніть це поле!'),
                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                           "Ім'я повинно містити тільки англійські літери, цифри, крапку або нижнє підкреслення!")
                    ]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(message='Заповніть це поле!'), Email(message='Некоректна email адреса!')]
    )
    password = PasswordField(
        'Пароль',
        validators=[Length(min=8, max=30,
                           message='Поле повинно бути довжиною від 3 до 30 симолів!'),
                    DataRequired(message='Заповніть це поле!')]
    )
    confirm_password = PasswordField(
        'Підтвердження паролю',
        validators=[DataRequired(message='Заповніть це поле!'),
                    EqualTo('password', message='Паролі не збігаються!')]
    )
    submit = SubmitField('Зареєструватись')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(
                'Користувач з таким email уже зареєстрований!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                "Користувач з таким ім'ям уже зареєстрований!")


