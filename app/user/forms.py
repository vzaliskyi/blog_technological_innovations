from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField(
                           'Username',
                           validators=[DataRequired('Це поле є обов\'язковим')]
                           )
    password = PasswordField(
                             'Password',
                             validators=[DataRequired('Це поле є обов\'язковим')]
                             )
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[Length(min=3, max=30,message='Поле повинно бути довжиною від 3 до 30 симолів!'),
        DataRequired(message="Це поле є обов'язковим!"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               "Ім'я повинно містити тільки англійські літери, цифри, крапку або нижнє підкреслення!")
        ]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(message='Некоректна email адреса!')]
    )
    password = PasswordField(
        'Password',
        validators=[Length(min=8,
        message='Поле повинно бути довжиною більше 8 символів!'),
                    DataRequired(message="Це поле є обов'язковим!")]
    )
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(), EqualTo('password', message='Паролі не збігаються!')]
    )
    submit = SubmitField('Sing up')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email уже існує!')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Користувач з таким ім'я вже існує!")