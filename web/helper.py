# coding=utf-8
import math
import os
from functools import wraps
import numpy as np
import cv2
from PIL import Image, ImageDraw
from flask import session, redirect, url_for, render_template
from web import db, app
from web.models import User, AnonUser
from config import basedir


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


def delta_resolution(width, height, w, h):
    return abs((width / height) - (w / h))


def calibrate_resolution(resolution, w, h):
    width = resolution[0]
    height = resolution[1]
    if (width / height) > (w / h):
        while True:
            height += 2
            if delta_resolution(width, height - 2, w, h) < delta_resolution(width, height, w, h):
                return [width, height]
    if (width / height) < (w / h):
        while True:
            width += 2
            if delta_resolution(width - 2, height, w, h) < delta_resolution(width, height, w, h):
                return [width, height]
    return [width, height]


def handle_parse(items, minX, minY, maxX, maxY, room):
    resolution = (maxX - minX, maxY - minY)
    new_resolution = calibrate_resolution(resolution, 16, 9)
    deltax = (new_resolution[0] - resolution[0]) / 2
    deltay = (new_resolution[1] - resolution[1]) / 2
    draw, room_map = create_map(resolution)
    for item in items:
        user, rect, color = item
        rect = ((rect[0][0] - minX, rect[0][1] - minY), rect[1], rect[2])
        save_parse(user, rect, deltax, deltay, new_resolution)
        draw_map(draw, rect, color)
    save_map(draw, room, room_map)


def draw_map(draw, rect, color):
    draw.polygon(np.int0(cv2.boxPoints(rect)).flatten().tolist(), fill=color)


def create_map(resolution):
    room_map = Image.new('RGB', resolution, (255, 255, 255))
    return ImageDraw.Draw(room_map), room_map


def save_map(draw, room, room_map):
    del draw
    filename = basedir + '/images/' + str(room.id) + '_map.jpg'
    if os.path.exists(filename):
        os.remove(filename)
    room_map.save(filename)


def save_parse(user, rect, deltax, deltay, new_resolution):
    if -95 < rect[2] < -85:
        firsty = int(rect[0][1] - rect[1][0] / 2) + deltay
        firstx = int(rect[0][0] - rect[1][1] / 2) + deltax
        lastx = int(rect[0][0] + rect[1][1] / 2) + deltax
    else:
        firsty = int(rect[0][1] - rect[1][1] / 2) + deltay
        firstx = int(rect[0][0] - rect[1][0] / 2) + deltax
        lastx = int(rect[0][0] + rect[1][0] / 2) + deltax
    width = (new_resolution[0] / (lastx - firstx)) * 100
    left = - (firstx / new_resolution[0]) * width
    top = - (firsty / new_resolution[1]) * width
    user.res_k = int(width)
    user.top = int(top)
    user.left = int(left)
    db.session.commit()


def parse(room, users, impath):
    img = cv2.imread(impath)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    items = list()
    maxX = maxY = -math.inf
    minY = minX = math.inf
    for user in users:
        R = int(user.color[1:3], 16)
        G = int(user.color[3:5], 16)
        B = int(user.color[5:7], 16)
        color = (B, G, R)
        hsv_color = np.array(color, dtype=np.uint8, ndmin=3)
        hue = cv2.cvtColor(hsv_color, cv2.COLOR_BGR2HSV).flatten()[0]
        h_min = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8)
        h_max = np.array([min(hue + 10, 179), 255, 255], dtype=np.uint8)
        thresh = cv2.inRange(hsv_img, h_min, h_max)
        _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rect = cv2.minAreaRect(sorted(contours, key=cv2.contourArea, reverse=True)[0])
        box = np.int0(cv2.boxPoints(rect))
        minX = min(minX, np.ndarray.min(box[..., 0]))
        maxX = max(maxX, np.ndarray.max(box[..., 0]))
        minY = min(minY, np.ndarray.min(box[..., 1]))
        maxY = max(maxY, np.ndarray.max(box[..., 1]))
        items.append([user, rect, (color[2], color[1], color[0])])
    handle_parse(items, minX, minY, maxX, maxY, room)


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
