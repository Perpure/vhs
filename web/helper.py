# coding=utf-8
import os
import cv2
from functools import wraps
from flask import session, redirect, url_for, render_template
from web import db, app
from web.models import User, AnonUser
from config import basedir
from web.parser import parse


def requiresauth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if cur_user() is None:
            return redirect(url_for('log'))
        return f(*args, **kwargs)

    return wrapped


def cur_user():
    if 'Login' in session:
        return User.get(login=session['Login'])
    return None


def anon_user():
    user = None
    if 'anon_id' in session:
        user = AnonUser.query.get(session['anon_id'])
    if not user:
        user = AnonUser()
        session['anon_id'] = user.id
    return user


def read_multi(pid):
    path = basedir + '/images/%s.jpg' % pid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def read_image(pid):
    path = basedir + '/video/%s/preview.png' % pid
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


def image_loaded(request, room, user, users, image_form, room_form):
    room_id = room.id
    room_map_filename = basedir + '/images/' + str(room_id) + '_map.jpg'
    room_map_url = str(room_id) + '_map'

    file = request.files['image']

    file.save(basedir + '/images/' + str(room_id) + '.' + file.filename.split('.')[-1].lower())
    try:
        parse(room, users, basedir + '/images/' + str(room_id) + '.jpg')
    except (cv2.error, IndexError, ValueError, TypeError) as e:
        return render_template('room.html', room=room, user=cur_user(), color=user.color, users=users,
                               image_form=image_form, count=len(users),
                               room_form=room_form, loaded=True, room_map=room_map_url, anon=user,
                               msg="Мы не смогли идентифицировать устройства,"
                                   " попробуйте загрузить другую фотографию.",
                               map_ex=os.path.exists(room_map_filename))
    else:
        return render_template('room.html', room=room, user=cur_user(), color=user.color, users=users,
                               image_form=image_form, anon=user,
                               room_form=room_form, loaded=True, room_map=room_map_url, count=len(users) + 1,
                               map_ex=os.path.exists(room_map_filename))
