from flask import session
from config import basedir
from werkzeug.exceptions import Aborter
from functools import wraps
from web.models import User


def read_image(pid):
    path = basedir + '/images/%s.jpg' % pid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def cur_user():
    if 'Login' in session:
        return User.query.get(session['Login'])
    else:
        return None


def requiresauth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if cur_user() is None:
            abort = Aborter()
            return abort(403)
        return f(*args, **kwargs)
    return wrapped
