# coding=utf-8
"""Данный файл описывает формы приложения"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FieldList, BooleanField, RadioField, FileField
from wtforms.validators import Length, EqualTo, ValidationError, DataRequired, Optional
from web.models import User
from .helper import cur_user
from wtforms.widgets import CheckboxInput, ListWidget

class RoomForm(FlaskForm):
    submit = SubmitField("Калибровка")

class UploadVideoForm(FlaskForm):
    title = StringField("Введите название видео", validators=[Length(3)])
    video = FileField("Выберите файл")
    submit = SubmitField("Загрузить")

class UploadImageForm(FlaskForm):
    image = FileField("Выберите файл")
    submit = SubmitField("Загрузить")

def not_exist(form, field):
    if User.get(login=field.data):
        raise ValidationError("Такой пользователь уже существует")


def exist(form, field):
    if User.get(login=field.data) is None:
        raise ValidationError("Такого пользователя не существует")


def match(form, field):
    if cur_user():
        user = cur_user()
    else:
        user = User.get(login=form.login_log.data)
    if (user is None) and (not user.check_pass(field.data)):
        raise ValidationError("Неправильный пароль")

            

class RegForm(FlaskForm):
    login_reg = StringField("Имя пользователя", validators=[Length(5), not_exist])
    password_reg = PasswordField("Пароль", validators=[Length(8)])
    confirm_reg = PasswordField("Повторите пароль",
                                validators=[Length(8), EqualTo("password_reg", message="Пароли должны совпадать")])
    submit_reg = SubmitField("Зарегистрироваться")
    submit_main = SubmitField("На главную")


class JoinForm(FlaskForm):
    token = StringField("Токен")
    submit = SubmitField("Присоединиться")


class LogForm(FlaskForm):
    """Форма авторизации"""
    login_log = StringField("Имя пользователя", validators=[Length(5), exist])
    password_log = PasswordField("Пароль", validators=[Length(8), match])
    submit_log = SubmitField("Войти")
    submit_main = SubmitField("На главную")


class UploadVideoForm(FlaskForm):
    """Форма загрузки видео"""
    title = StringField("Введите название видео", validators=[Length(3)])
    video = FileField("Выберите файл")
    submit = SubmitField("Загрузить")


class UserProfileForm(FlaskForm):
    """Форма редактирования профиля пользователя"""
    change_name = StringField("Изменить имя:", validators=[Length(3), Optional()])
    change_password = PasswordField("Изменить пароль:", validators=[Length(8), Optional()])
    change_avatar = FileField("Изменить аватар профиля:")
    change_background = FileField("Изменить фон канала:")
    channel_info = StringField("Указать информацию о канале:",
                               validators=[Length(8), Optional()])
    current_password = PasswordField("Введите свой текущий пароль для подтверждения изменений:",
                                     validators=[Length(8), match])
    submit_changes = SubmitField("Сохранить")

