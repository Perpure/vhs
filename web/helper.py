# coding=utf-8
import os
import cv2
from functools import wraps
from flask import session, redirect, url_for, render_template
from web import db, app
from web.models import User, Device
from config import basedir
from web.parser import parse
from flask.json import dumps


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['v'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


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
        user = Device.query.get(session['anon_id'])
    if not user:
        user = Device()
        session['anon_id'] = user.id
    return user


def read_multi(pid):
    path = basedir + '/images/%s.jpg' % pid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def read_image(pid):
    path = app.config['VIDEO_SAVE_PATH'] + '/%s/preview.png' % pid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def image_loaded(request, room, user, users, image_form, room_form):
    room_id = room.id
    room_map_url = str(room_id) + '_map'
    file = request.files['image']
    file.save(basedir + '/images/' + str(room_id) + '.' + file.filename.split('.')[-1].lower())
    image_path = basedir + '/images/' + str(room_id) + '.jpg'
    msg = True
    if not parse(room, users, image_path):
        msg = False
    return dumps({'status': msg, 'map_url': url_for('get_multi', pid=room_map_url)})


def decode_iso8601_duration(duration):
    x = ''
    data = {}
    res = ''

    for char in duration[2:]:
        if char in ['H', 'M', 'S']:
            data.update({char: x})
            x = ''
        else:
            x += char
    if data.get('H') is not None:
        res += data.get('H') + ' час. '
    if data.get('M') is not None:
        res += data.get('M') + ' мин. '
    if data.get('S') is not None:
        res += data.get('S') + ' сек.'

    return res
