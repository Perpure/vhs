# coding=utf-8
"""Данный файл содержит функции для "/разгрузки"/ контроллера"""
from functools import wraps
from flask import session
from werkzeug.exceptions import Aborter
from config import basedir
from web.models import User
from web import ALLOWED_EXTENSIONS


def read_image(pid):
    """

    :param pid:
    :return:
    """
    path = basedir + '/images/%s.jpg' % pid
    with open(path, "rb") as image:
        file = image.read()
        b_arr = bytearray(file)
        return b_arr


def cur_user():
    """
    Функция для вывода текущего пользователя
    :return: Текущий пользователь или None
    """
    if 'Login' in session:
        return User.query.get(session['Login'])
    return None


def requiresauth(f):
    """Обёртка декоратора"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        """
        Декоратор, проверяющий авторизацию пользователя
        :param f:
        :return: В случае, если пользователь не авторизован - вызывает исключение 403
        """
        if cur_user() is None:
            abort = Aborter()
            return abort(403)
        return f(*args, **kwargs)
    return wrapped


def allowed_file(filename):
    """
    Проверяет, является ли расширение файла разрешённым
    :param filename: Название загружаемого файла
    :return:
    """
    return ('.' in filename and
            filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS)
