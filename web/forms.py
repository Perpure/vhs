from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, ValidationError
from web.models import User


def NotExist(form, field):
    if User.get(login=field.data):
        raise ValidationError("Такой пользователь уже существует")


def Exist(form, field):
    if not User.get(login=field.data):
        raise ValidationError("Такого пользователя не существует")


def Match(form, field):
    user = User.get(login=form.login_log.data)
    if user and not user.check_pass(field.data):
        raise ValidationError("Неправильный пароль")


class RegForm(FlaskForm):
    login_reg = StringField("Имя пользователя", validators=[Length(5), NotExist])
    password_reg = PasswordField("Пароль", validators=[Length(8)])
    confirm_reg = PasswordField("Повторите пароль",
                                validators=[Length(8), EqualTo("password_reg", message="Пароли должны совпадать")])
    submit_reg = SubmitField("Зарегистрироваться")


class LogForm(FlaskForm):
    login_log = StringField("Имя пользователя", validators=[Length(5), Exist])
    password_log = PasswordField("Пароль", validators=[Length(8), Match])
    submit_log = SubmitField("Войти")