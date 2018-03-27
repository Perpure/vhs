from config import basedir
from flask import session
from web.models import User


def read_multi(pid):
    path=basedir + '/images/%s.jpg' % pid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def read_image(pid):
    path=basedir + '/video/%s/preview.png' % pid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def read_video(vid):
    path = basedir + '/video/%s/video.mp4' % vid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def is_true_pixel(r,g,b,R,G,B):
    return (r in range(R-50,R+50))and(g in range(G-50,G+50))and(b in range(B-50,B+50))


def cur_user():
    if 'Login' in session:
        return User.get(login=session['Login'])
    return None


class IsVideoViewed:
    # костыль для просмотров, этот класс лучше не трогать
    is_viewed = []
    request = ""

