from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import SelectField
from wtforms.fields.simple import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class FilmForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired("Поле не должно быть пустым")])
    description = TextAreaField('Описание', validators=[DataRequired("Поле не должно быть пустым")])
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'jpeg', 'png'], message='Неверный формат изображения'),
                                                 FileRequired(message='Поле не должно быть пустым')])
    submit = SubmitField("Добавить фильм")


class ReviewForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired("Поле не должно быть пустым")])
    text = TextAreaField("Текст отзыва", validators=[DataRequired("Поле не должно быть пустым")])
    score = SelectField('Оценка', choices=[(str(i), str(i)) for i in range(1, 11)],
                        validators=[DataRequired("Поле не должно быть пустым")])
    submit = SubmitField("Добавить отзыв")
