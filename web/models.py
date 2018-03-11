from web import db
from web import app
import uuid
import hashlib
import os
from datetime import datetime, date, time


class Video(db.Model):
    title = db.Column(db.String(100))
    path = db.Column(db.Text(),  nullable=False)
    id = db.Column(db.Text(), primary_key=True)
    date = db.Column(db.DateTime)

    def __init__(self, title):
        self.title = title

    def save(self, hash, ext):
        self.date = datetime.now(tz=None)
        self.id = hashlib.md5(
            (hash + self.date.isoformat()).encode("utf-8")).hexdigest()
        self.path = os.path.join(app.config['VIDEO_SAVE_PATH'], hash+'.'+ext)

        db.session.add(self)
        db.session.commit()

        return self.path

    @staticmethod
    def get(hash=None):
        if hash is None:
            return Video.query.all()
        return Video.query.get(hash)


class User(db.Model):
    login = db.Column(db.String(32), nullable=False, primary_key=True)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, login):
        self.login = login

    def save(self, password):
        self.password = hashlib.sha512(
            password.encode("utf-8")).hexdigest()
        db.session.add(self)
        db.session.commit()

    def check_pass(self, password):
        temp = User.query.get(self.login)
        return temp and temp.password == hashlib.sha512(
            password.encode("utf-8")).hexdigest()

    @staticmethod
    def get(login=None):
        if not login:
            return User.query.all()
        return User.query.get(login)
