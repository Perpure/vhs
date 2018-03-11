from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import Length, EqualTo, ValidationError
from web.models import User


def NotExist(form, field):
    if User.get(login=field.data):
        raise ValidationError("Такой пользователь уже существует")


def Exist(form, field):
    user = User.query.filter_by(login=field.data).first()
    if not user:
        raise ValidationError("Такого пользователя не существует")


def Match(form, field):
    user = User.query.filter_by(login=field.data).first()
    if user and not user.check_pass(field.data):
        raise ValidationError("Неправильный пароль")


class RegForm(FlaskForm):
    login_reg = StringField("Имя пользователя",
                            validators=[Length(5), NotExist])
    password_reg = PasswordField("Пароль", validators=[Length(8)])
    confirm_reg = PasswordField(
        "Повторите пароль", validators=[Length(8), EqualTo(
            "password_reg", message="Пароли должны совпадать")])
    submit_reg = SubmitField("Зарегистрироваться")
    submit_main = SubmitField("На главную")


class LogForm(FlaskForm):
    login_log = StringField("Имя пользователя", validators=[Length(5), Exist])
    password_log = PasswordField("Пароль", validators=[Length(8), Match])
    submit_log = SubmitField("Войти")
    submit_main = SubmitField("На главную")


class UploadVideoForm(FlaskForm):
    title = StringField("Введите название видео", validators=[Length(3)])
    video = FileField("Выберите файл")
    submit = SubmitField("Загрузить")
