from web import db
import hashlib


class User(db.Model):
    login = db.Column(db.String(32), nullable=False, primary_key=True)
    password = db.Column(db.String(64), nullable=False)

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
