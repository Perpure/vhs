from web import db
from web import app
import uuid
import hashlib
import os
from datetime import datetime, date, time


class Marks(db.Model):
    id = db.Column(db.Text(), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    is_like = db.Column(db.Boolean, nullable=False)

    def save(self,is_like):
        self.is_like = is_like
        db.session.add(self)
        db.session.commit()

association_table = db.Table('association', db.Model.metadata,
    db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('Room_id', db.Integer, db.ForeignKey('Room.id'))
)


association_table2 = db.Table('association2', db.Model.metadata,
    db.Column('Color_id', db.Integer, db.ForeignKey('Color.id')),
    db.Column('Room_id', db.Integer, db.ForeignKey('Room.id'))
)

class Video(db.Model):
    """Класс описывающий модель Видео"""
    title = db.Column(db.String(100))
    path = db.Column(db.Text(), nullable=False)
    id = db.Column(db.Text(), primary_key=True)
    date = db.Column(db.DateTime)
    views = db.Column(db.Integer())
    user = db.Column(db.Integer())

    marks = db.relationship('Marks', backref='video', lazy=True)
    comments = db.relationship('Comment', backref='video', lazy='joined')

    def __init__(self, title):
        self.title = title
        self.views = 0

    def save(self, hash, user):
        self.date = datetime.now(tz=None)
        self.id = hashlib.md5((hash + self.date.isoformat()).encode("utf-8")).hexdigest()
        self.path = os.path.join(app.config['VIDEO_SAVE_PATH'], self.id)
        self.user = user

        db.session.add(self)
        db.session.commit()

        return self.path

    # def add_view(self):
    #     self.views += 1
    #     db.session.add(self)
    #     db.session.commit()

    @staticmethod
    def get(video_id=None):
        if video_id is None:
            return Video.query.all()
        return Video.query.get(video_id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    video_id = db.Column(db.Text(), db.ForeignKey('video.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, text, video_id, user_id):
        self.text = text
        self.user_id = user_id
        self.video_id = video_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    channel_info = db.Column(db.String(64))
    Action = db.Column(db.String(64))
    views_limit = 0

    marks = db.relationship('Marks', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy='joined')
    Room = db.relationship("Room",
                secondary = association_table,
                backref = "User",
                lazy = 'dynamic')
    
    def __init__(self, login):
        self.login = login
        self.name = login
        self.channel_info = "channel_info"

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
        hash = hashlib.sha512(password.encode("utf-8")).hexdigest()
        return self.password == hash

    def change_name(self, name):
        """
        Метод, изменяющий имя пользователя
        :param name: Имя пользователя
        """
        self.name = name
        db.session.add(self)
        db.session.commit()

    def change_channel_info(self, info):
        """
        Метод, изменяющий информацию о канале пользователя
        :param info: Информация о канале
        """
        self.channel_info = info
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id=None, login=None):
        if login:
            return User.query.filter_by(login=login).first()
        if id:
            return User.query.get(id)
        return User.query.all()


class Room(db.Model):
    __tablename__ = 'Room'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(64), nullable=False)
    color_user = db.Column(db.Text())
    Color = db.relationship("Color",
                secondary=association_table2,
                backref="Room",
                lazy='dynamic')


class Color(db.Model):
    __tablename__ = 'Color'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String(64), nullable=False)
