# coding=utf-8
"""Данный файл описывает модели базы даннных"""
import hashlib
import os
from datetime import datetime
from web import db
from web import app


class Video(db.Model):
    """Класс описывающий модель Видео"""
    title = db.Column(db.String(100))
    path = db.Column(db.Text(), nullable=False)
    id = db.Column(db.Text(), primary_key=True)
    date = db.Column(db.DateTime)

    def __init__(self, title):
        self.title = title

    def save(self, video_hash, ext):
        """
        Функция сохранения нового видео в базе данных
        :param video_hash: Хеш видео
        :param ext: Имя видео
        :return: Путь к видео
        """
        self.date = datetime.now(tz=None)
        self.id = hashlib.md5(
            (video_hash + self.date.isoformat()).encode("utf-8")).hexdigest()
        self.path = os.path.join(app.config['VIDEO_SAVE_PATH'], video_hash + '.' + ext)

        db.session.add(self)
        db.session.commit()

        return self.path

    @staticmethod
    def get(video_hash=None):
        """
        Метод, получающий видео из хеша
        :param video_hash:
        :return:
        """
        if video_hash is None:
            return Video.query.all()
        return Video.query.get(video_hash)


class User(db.Model):
    """Класс описывающий модель Пользователя"""
    login = db.Column(db.String(32), nullable=False, primary_key=True)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, login):
        self.login = login

    def save(self, password):
        """
        Функция сохранения нового пользователя в базе данных
        :param password: Пароль
        """
        self.password = hashlib.sha512(
            password.encode("utf-8")).hexdigest()
        db.session.add(self)
        db.session.commit()

    def check_pass(self, password):
        """
        Функция проверяющая соответствие пароля введённого пользователем
        :param password: Введённый пароль
        :return: True если соответствует, иначе False
        """
        temp = User.query.get(self.login)
        return temp and temp.password == hashlib.sha512(
            password.encode("utf-8")).hexdigest()

    @staticmethod
    def get(login=None):
        """
        Метод, возвращающий пользователя по логину
        :param login: Логин пользователя
        :return: Пользователь
        """
        if not login:
            return User.query.all()
        return User.query.get(login)
