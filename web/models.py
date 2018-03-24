from web import db
from web import app
import uuid
import hashlib
import os
from datetime import datetime, date, time


likes = db.Table('likes', db.Model.metadata,
                db.Column('user_login', db.String(32), db.ForeignKey('User.login'), 
                    nullable=False, primary_key=True),
                db.Column('video_id', db.Text(), db.ForeignKey('video.id'), 
                    nullable=False, primary_key=True))

dislikes = db.Table('dislikes', 
                db.Column('user_login', db.String(32), db.ForeignKey('User.login'), 
                    nullable=False, primary_key=True),
                db.Column('video_id', db.Text(), db.ForeignKey('video.id'), 
                    nullable=False, primary_key=True))


association_table = db.Table('association', db.Model.metadata,
    db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('Room_id', db.Integer, db.ForeignKey('Room.id'))
)

association_table2 = db.Table('association2', db.Model.metadata,
    db.Column('Color_id', db.Integer, db.ForeignKey('Color.id')),
    db.Column('Room_id', db.Integer, db.ForeignKey('Room.id'))
)

class Video(db.Model):
    title = db.Column(db.String(100))
    path = db.Column(db.Text(), nullable=False)
    id = db.Column(db.Text(), primary_key=True)
    date = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='video', lazy='joined')

    likes = db.relationship('User', secondary=likes, lazy=False,
                            backref=db.backref('liked', lazy=False))

    dislikes = db.relationship('User', secondary=dislikes, lazy=False,
                               backref=db.backref('disliked', lazy=False))

    def __init__(self, title):
        self.title = title

    def save(self, hash):
        self.date = datetime.now(tz=None)
        self.id = hashlib.md5((hash + self.date.isoformat()).encode("utf-8")).hexdigest()
        self.path = os.path.join(app.config['VIDEO_SAVE_PATH'], self.id)

        db.session.add(self)
        db.session.commit()

        return self.path

    @staticmethod
    def get(video_id=None):
        if video_id is None:
            return Video.query.all()
        return Video.query.get(video_id)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'),nullable=False)
    user_login = db.Column(db.Integer, db.ForeignKey('User.login'), nullable=False)

    def __init__(self, text, video_id, user_login):
        self.text = text
        self.user_login = user_login
        self.video_id = video_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy='joined')
    Room = db.relationship("Room",
                secondary=association_table,
                backref="User",
                lazy='dynamic')
    Action = db.Column(db.String(64))
    def __init__(self, login):
        self.login = login

    def save(self, password):
        self.password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        db.session.add(self)
        db.session.commit()

    def check_pass(self, password):
        temp = User.query.get(self.login)
        return temp and temp.password == hashlib.sha512(password.encode("utf-8")).hexdigest()

    @staticmethod
    def get(login=None):
        if not login:
            return User.query.all()
        return User.query.get(login)

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
