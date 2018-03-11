from web import db
from web import app
import uuid
import hashlib
import os
from datetime import datetime, date, time



association_table = db.Table('association', db.Model.metadata,
    db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('Room_id', db.Integer, db.ForeignKey('Room.id'))
)

class Video(db.Model):
    title = db.Column(db.String(100))
    path = db.Column(db.Text(),  nullable=False)
    id = db.Column(db.Text(), primary_key=True)
    date = db.Column(db.DateTime)

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




class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    Room = db.relationship("Room",
                secondary=association_table,
                backref="User")
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

