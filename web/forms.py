﻿# coding=utf-8
"""Данный файл описывает формы приложения"""
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, FileField, HiddenField
from wtforms.validators import Length, EqualTo, ValidationError, DataRequired, Optional, Email
from flask.json import JSONDecoder
from flask_wtf.file import FileAllowed
from web.models import User, Room
from .helper import cur_user
from web import avatars, backgrounds, app


class RoomForm(FlaskForm):
    submit = SubmitField("Калибровка")


class UploadImageForm(FlaskForm):
    class Meta:
        csrf = False

    image = FileField("Выберите файл", validators=[FileAllowed(app.config['ALLOWED_IMAGE_EXTENSIONS'],
                                                               message="Некорректное расширение"),
                                                   DataRequired(message='Выберите изображение')])
    submit = SubmitField("Инициализировать фотографию")


def exist(form, field):
    if User.get(login=field.data):
        raise ValidationError("Такой пользователь уже существует")


def not_exist(form, field):
    if User.get(login=field.data) is None:
        raise ValidationError("Такого пользователя не существует")


def exist_token(form, field):
    if Room.query.filter_by(name=field.data).first():
        raise ValidationError("Такая комната уже существует")


def not_exist_token(form, field):
    if not Room.query.filter_by(name=field.data).first():
        raise ValidationError("Такой комнаты нет")


def check_correct_name(form, field):
    if not re.match(r'[a-zA-Z0-9_]', field.data):
        raise ValidationError("В имени пользователя могут быть только цифры, латинские буквы и нижние подчёркивания")


def match(form, field):
    user = None
    if cur_user():
        user = cur_user()
    elif form.login_log.data is not '':
        user = User.get(login=form.login_log.data)
    if user and not user.check_pass(field.data):
        raise ValidationError("Неправильный пароль")


def have_geodata(form, field):
    data = JSONDecoder().decode(field.data)
    if data['needed'] and not data['coords']:
        raise ValidationError("Выставьте геотег")


class RegForm(FlaskForm):
    login_reg = StringField("Имя пользователя", validators=[Length(5, message='Логин слишком короткий'),
                                                            exist, check_correct_name])
    password_reg = PasswordField("Пароль", validators=[Length(8, message='Пароль слишком короткий')])
    confirm_reg = PasswordField("Повторите пароль",
                                validators=[Length(8, message='Пароль слишком короткий'),
                                            EqualTo("password_reg", message="Пароли должны совпадать")])
    submit_reg = SubmitField("Зарегистрироваться")
    submit_main = SubmitField("На главную")


class JoinForm(FlaskForm):
    class Meta:
        csrf = False

    token = StringField("Название комнаты", validators=[not_exist_token, Length(2,
                                                                                message='Название слишком короткое')])
    submit = SubmitField("Присоединиться")


class LogForm(FlaskForm):
    """Форма авторизации"""
    login_log = StringField("Имя пользователя", validators=[Length(5, message='Логин слишком короткий'),
                                                            check_correct_name, not_exist])
    password_log = PasswordField("Пароль", validators=[Length(8, message='Пароль слишком короткий'),
                                                       match])
    submit_log = SubmitField("Войти")
    submit_main = SubmitField("На главную")


class UploadVideoForm(FlaskForm):
    """Форма загрузки видео"""

    title = StringField("Введите название видео", validators=[Length(3, message='Название слишком короткое')])
    video = FileField("Выберите файл", validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'],
                                                               message="Некорректное расширение"),
                                                   DataRequired(message='Выберите видео')])
    geotag_data = HiddenField(validators=[have_geodata])
    tags = TextAreaField("Текстовые теги", validators=[Length(2, message='Тэг слишком короткий'), Optional()])
    submit = SubmitField("Загрузить")


class UserProfileForm(FlaskForm):
    """Форма редактирования профиля пользователя"""
    change_name = StringField("Изменить имя:", validators=[Length(3, message='Имя слишком короткое'), Optional()])
    background = FileField("Изменить фон канала:", validators=[FileAllowed(backgrounds,
                                                                           message="Некорректное расширение")])
    avatar = FileField("Изменить аватар профиля:", validators=[FileAllowed(avatars,
                                                                           message="Некорректное расширение")])
    channel_info = TextAreaField("Указать краткое описание канала:",
                                 validators=[Length(8, message='Текст слишком короткий'), Optional()])
    current_password = PasswordField("Введите свой текущий пароль для подтверждения изменений:",
                                     validators=[Length(8, message='Пароль слишком короткий'), match])
    submit_changes = SubmitField("Сохранить")


class AccountSettingsForm(FlaskForm):
    """Форма редактирования аккаунта пользователя"""
    change_password = PasswordField("Изменить пароль:", validators=[Length(8, message='Пароль слишком короткий'),
                                                                    Optional()])
    cur_password = PasswordField("Введите свой текущий пароль для подтверждения изменений:",
                                 validators=[Length(8, message='Пароль слишком короткий'), match])
    save_changes = SubmitField("Сохранить")


class SearchingVideoForm(FlaskForm):
    """Форма поиска видео"""
    search = StringField("Название")
    date = BooleanField("Дата")
    views = BooleanField("Просмотры")
    submit = SubmitField("Поиск")


class VideoToRoomForm(FlaskForm):
    submit = SubmitField("Создать комнату для видео")


class AddRoomForm(FlaskForm):
    class Meta:
        csrf = False

    token = StringField("Название комнаты", validators=[DataRequired(message='Введите название комнаты'),
                                                        exist_token,
                                                        Length(2, message='Текст слишком короткий')])
    submit = SubmitField("Создать")


class FeedbackForm(FlaskForm):
    feedback_email = StringField('Ваш email', validators=[DataRequired(message='Введите email'),
                                                          Email(message='Введите корректный email'),
                                                          Length(max=32, message='Слишком длинный email')])
    feedback_text = TextAreaField('Ваше сообщение', validators=[DataRequired(message='Сообщение не должно быть пустым'),
                                                                Length(min=5, max=250,
                                                                       message='Сообщение должно быть не '
                                                                               'меньше 5 и не больше 250 символов')])
    feedback_submit = SubmitField('Отправить')
