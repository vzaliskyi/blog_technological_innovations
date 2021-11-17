from .models import Category, Post
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, TextAreaField,
                     ValidationError)
from wtforms.validators import DataRequired, Length


# def title_duplicate(form, field):
#     if Post.query.filter_by(title=field.data).first():
#         raise ValidationError('Ви вже створювали публікацію з такою самою '
#                               'назвою!')


class FormPostCreate(FlaskForm):
    category = SelectField(
        'Категорія',
        coerce=int
    )
    title = StringField(
        "Заголовок",
        validators=[Length(min=5, max=100,
                           message='Заголовок повинен бути довжиною '
                                   'від 5 до 100 симолів!'),
                    DataRequired(message='Заповніть це поле!')]
    )
    content = TextAreaField(
        'Вміст',
        validators=[
            DataRequired()
        ],
        # render_kw={'cols':35, 'rows': 5}
    )
    submit = SubmitField('Створити')

    def validate_title(self, field):
        if Post.query.filter_by(title=field.data).first():
            raise ValidationError(
                'Ви вже створювали публікацію з такою самою назвою!')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the agency field
        form.category.choices = [(elem.id, elem.name) for elem in
                                 Category.query.all()]
        return form


class FormPostUpdate(FlaskForm):
    category = SelectField(
        'Категорія',
        coerce=int
    )
    title = StringField(
        "Заголовок",
        validators=[Length(min=5, max=100,
                           message='Заголовок повинен бути довжиною '
                                   'від 5 до 100 симолів!'),
                    DataRequired(message='Публікація повинна мати заголовок')]
    )
    content = TextAreaField(
        'Контент',
        validators=[
            DataRequired(message='Вміст публікації не може бути порожнім')
        ],
        # render_kw={'cols':35, 'rows': 5}
    )
    submit = SubmitField('Оновити')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the agency field
        form.category.choices = [(elem.id, elem.name) for elem in
                                 Category.query.all()]
        return form
