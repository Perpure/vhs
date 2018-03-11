from web import db
import uuid
import hashlib

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    path = db.Column(db.Text(),  nullable=False)

    def __init__(self, title, path):
        self.title = title
        self.path = path

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id=None):
        if id == None: return Video.query.all()
        return Video.query.get(id)

class User(db.Model):
    login = db.Column(db.String(32), nullable=False, primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    rooms = db.Column(db.Text())

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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(64), nullable=False)

