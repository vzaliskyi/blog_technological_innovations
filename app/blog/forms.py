from .models import Category
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class FormPostCreate(FlaskForm):
    category = SelectField(
        'Категорія',
        coerce=int
    )
    title = StringField(
        "Заголовок",
        validators=[Length(min=1, max=100,
                           message='Поле повинно бути довжиною '
                                   'від 1 до 100 симолів!'),
                    DataRequired(message='Заповніть це поле!')]
    )
    content = TextAreaField(
        'Контент',
        validators=[
            DataRequired()
        ],
        # render_kw={'cols':35, 'rows': 5}
    )
    submit = SubmitField('Створити')

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
        validators=[Length(min=1, max=100,
                           message='Поле повинно бути довжиною '
                                   'від 1 до 100 симолів!'),
                    DataRequired(message='Заповніть це поле!')]
    )
    content = TextAreaField(
        'Контент',
        validators=[
            DataRequired()
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
