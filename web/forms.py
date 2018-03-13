# coding=utf-8
"""Данный файл описывает формы приложения"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, FileField
from wtforms.validators import Length, EqualTo, ValidationError
from web.models import User


def not_exist(form, field):
    """
    Функция проверяющая уникальность пользователя
    :param form: форма
    :param field: поле
    """
    if User.get(login=field.data):
        raise ValidationError("Такой пользователь уже существует")


def exist(form, field):
    """
    Функция проверяющая уникальность пользователя
    :param form: форма
    :param field: поле
    """
    user = User.query.filter_by(login=field.data).first()
    if not user:
        raise ValidationError("Такого пользователя не существует")


def match(form, field):
    """
    Функция проверяющая правильность пароля пользователя
    :param form: форма
    :param field: поке
    """
    user = User.query.filter_by(login=field.data).first()
    if user and not user.check_pass(field.data):
        raise ValidationError("Неправильный пароль")


class RegForm(FlaskForm):
    """Форма регистрации"""
    login_reg = StringField("Имя пользователя",
                            validators=[Length(5), not_exist])
    password_reg = PasswordField("Пароль", validators=[Length(8)])
    confirm_reg = PasswordField(
        "Повторите пароль", validators=[Length(8), EqualTo(
            "password_reg", message="Пароли должны совпадать")])
    submit_reg = SubmitField("Зарегистрироваться")
    submit_main = SubmitField("На главную")


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
    change_name = StringField("Изменить имя:", validators=[Length(3)])
    change_password = PasswordField("Изменить пароль:", validators=[Length(8)])
    change_avatar = FileField("Изменить аватар профиля:")
    change_background = FileField("Изменить фон канала:")
    channel_info =StringField("Указать информацию о канале:",
                                 validators=[Length(8)])
    current_password = PasswordField("Введите свой текущий пароль для подтверждения изменений:",
                                     validators=[Length(8)])
    submit_changes = SubmitField("Сохранить")
