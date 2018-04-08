﻿from web import db
from web import app
import hashlib
import os
from datetime import datetime


UserToRoom = db.Table('UserToRoom', db.Model.metadata,
    db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('Room_id', db.Integer, db.ForeignKey('Room.id'))
)


ColorToRoom = db.Table('ColorToRoom', db.Model.metadata,
    db.Column('Color_id', db.Integer, db.ForeignKey('Color.id')),
    db.Column('Room_id', db.Integer, db.ForeignKey('Room.id'))
)


Views = db.Table('Views', db.Model.metadata,
    db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('Video_id', db.String(32), db.ForeignKey('Video.id'))
)

class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text())
    video_id = db.Column(db.Text(), db.ForeignKey('Video.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, text, video_id, user_id):
        self.text = text
        self.user_id = user_id
        self.video_id = video_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Mark(db.Model):
    __tablename__ = 'Mark'
    id = db.Column(db.Text(), primary_key=True)
    video_id = db.Column(db.String(32), db.ForeignKey('Video.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    is_like = db.Column(db.Boolean, nullable=False)

    def save(self,is_like):
        self.is_like = is_like
        db.session.add(self)
        db.session.commit()


class Video(db.Model):
    """Класс описывающий модель Видео"""
    __tablename__ = 'Video'
    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(140))
    path = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime)
    user = db.Column(db.Integer())

    marks = db.relationship('Mark', 
                    backref='video', 
                    lazy=True)

    comments = db.relationship('Comment',
                    backref='video', 
                    lazy='joined')

    viewers = db.relationship('User',
                    secondary=Views,
                    backref='views', 
                    lazy='joined')

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

    def add_viewer(self, user):
        self.viewers.append(user)
        
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(sort=None, video_id=None):
        if video_id:
            return Video.query.get(video_id)

        videos = Video.query.all()
        if sort:
            sort = s.lower()
            if "date" in sort: 
                videos.sort(key=lambda x: x.date, reverse=True)
            if "views" in sort:
                videos.sort(key=lambda x: x.views, reverse=True)
        return videos


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    channel_info = db.Column(db.String(64))
    Action = db.Column(db.String(64))

    marks = db.relationship('Mark',
                            backref='user',
                            lazy="joined")

    comments = db.relationship('Comment',
                               backref='user',
                               lazy='joined')

    rooms = db.relationship("Room",
                secondary = UserToRoom,
                backref = "user",
                lazy = 'joined')
    
    room_capitan = db.relationship("Room", backref='captain')

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
    capitan_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    token = db.Column(db.String(64), nullable=False)
    color_user = db.Column(db.Text())
    Color = db.relationship("Color",
                            secondary=ColorToRoom,
                            backref="Room",
                            lazy="joined")


class Color(db.Model):
    __tablename__ = 'Color'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String(64), nullable=False)
