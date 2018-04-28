# coding=utf-8
"""Данный файл описывает формы приложения"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FieldList, BooleanField, RadioField, FileField, HiddenField
from wtforms.validators import Length, EqualTo, ValidationError, DataRequired, Optional
from web.models import User , Room
from .helper import cur_user
from wtforms.widgets import CheckboxInput, ListWidget


class RoomForm(FlaskForm):
    submit = SubmitField("Калибровка")


class UploadImageForm(FlaskForm):
    image = FileField("Выберите файл")
    submit = SubmitField("Загрузить")


def not_exist(form, field):
    if User.get(login=field.data):
        raise ValidationError("Такой пользователь уже существует")


def exist(form, field):
    if User.get(login=field.data) is None:
        raise ValidationError("Такого пользователя не существует")

def exist_token(form,field):
    if Room.get(token=field.data):
        raise ValidationError("Такая комната уже существует")

def match(form, field):
    user = None
    if cur_user():
        user = cur_user()
    elif form.login_log.data is not '':
        user = User.get(login=form.login_log.data)
    if user and not user.check_pass(field.data):
        raise ValidationError("Неправильный пароль")

def have_geodata(form, field):
    if form.geotag_is_needed.data:
        try:
            [float(x) for x in field.data.split(',')]
        except Exception:
            raise ValidationError("Выставите геотег")


class RegForm(FlaskForm):
    login_reg = StringField("Имя пользователя", validators=[Length(5, message='Логин слишком короткий'),
                                                            not_exist])
    password_reg = PasswordField("Пароль", validators=[Length(8, message='Пароль слишком короткий')])
    confirm_reg = PasswordField("Повторите пароль",
                                validators=[Length(8, message='Пароль слишком короткий'),
                                            EqualTo("password_reg", message="Пароли должны совпадать")])
    submit_reg = SubmitField("Зарегистрироваться")
    submit_main = SubmitField("На главную")


class JoinForm(FlaskForm):
    token = StringField("Токен")
    submit = SubmitField("Присоединиться")


class LogForm(FlaskForm):
    """Форма авторизации"""
    login_log = StringField("Имя пользователя", validators=[Length(5, message='Логин слишком короткий'), exist])
    password_log = PasswordField("Пароль", validators=[Length(8, message='Пароль слишком короткий'),
                                                       match])
    submit_log = SubmitField("Войти")
    submit_main = SubmitField("На главную")


class UploadVideoForm(FlaskForm):
    """Форма загрузки видео"""
    title = StringField("Введите название видео", validators=[Length(3, message='Название слишком короткое')])
    video = FileField("Выберите файл")
    geotag_is_needed = BooleanField('Прикрепить геотег?')
    geotag_data = HiddenField(validators=[have_geodata])
    submit = SubmitField("Загрузить")


class UserProfileForm(FlaskForm):
    """Форма редактирования профиля пользователя"""
    change_name = StringField("Изменить имя:", validators=[Length(3, message='Имя слишком короткое'), Optional()])
    change_password = PasswordField("Изменить пароль:", validators=[Length(8, message='Пароль слишком короткий'),
                                                                    Optional()])
    change_avatar = FileField("Изменить аватар профиля:")
    change_background = FileField("Изменить фон канала:")
    channel_info = StringField("Указать информацию о канале:",
                               validators=[Length(8, message='Текст слишком короткий'), Optional()])
    current_password = PasswordField("Введите свой текущий пароль для подтверждения изменений:",
                                     validators=[Length(8, message='Пароль слишком короткий'), match])
    submit_changes = SubmitField("Сохранить")


class SearchingVideoForm(FlaskForm):
    """Форма поиска видео"""
    search = StringField("Название")
    date = BooleanField("Дата")
    views = BooleanField("Просмотры")
    submit = SubmitField("Поиск")


class AddCommentForm(FlaskForm):
    class Meta:
        csrf = False

    message = TextAreaField("Комментарий", validators=[DataRequired(message='Введите текст'),
                                                       Length(3, message='Текст слишком короткий')])
    submit = SubmitField("Запостить")


class AddTagForm(FlaskForm):
    name = TextAreaField("Тэги", validators=[Length(1, message='Тэг слишком короткий'), Optional()])



class AddRoomForm(FlaskForm):
    token = StringField("Название комнаты", validators=[DataRequired(),exist_token,Length(5, message='Текст слишком короткий')])
    submit = SubmitField("Создать")
