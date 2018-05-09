from config import basedir
from web import db, app
from web.models import User
from PIL import Image, ImageDraw, ImageEnhance
from web.models import User
from web import app
from functools import wraps
from flask import session, redirect, url_for
import numpy as np
import math
import cv2
import os

def allowed_image(filename):
    return ('.' in filename and
            filename.split('.')[-1].lower() in app.config["ALLOWED_IMAGE_EXTENSIONS"])

def allowed_file(filename):
    return ('.' in filename and
            filename.split('.')[-1].lower() in app.config["ALLOWED_EXTENSIONS"])

def requiresauth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if cur_user() is None:
            return redirect(url_for('log'))
        return f(*args, **kwargs)

    return wrapped

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


def is_true_pixel(r, g, b, R, G, B):
    k=60
    return (r in range(R-k, R+k))and(g in range(G-k, G+k))and(b in range(B-k, B+k))


def parse(room, users, impath):
    img = cv2.imread(impath) # Читаем изображение
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Меняем цветовую схему с BGR на HSV

    rects = list()

    maxX = maxY = -math.inf
    minY = minX = math.inf
    
    for user in users:
        R = int(user.color[1:3], 16)
        G = int(user.color[3:5], 16)
        B = int(user.color[5:7], 16)
        color = (B,G,R)
        # Меняем схему цвета на HSV
        hsv_color = np.array(color, dtype=np.uint8, ndmin=3) 
        # Достаём из него только Hue
        hue = cv2.cvtColor(hsv_color, cv2.COLOR_BGR2HSV).flatten()[0] 

        # Создаём минимальный предел
        h_min = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8) 
        # И максимальный
        h_max = np.array([min(hue + 10, 179), 255, 255], dtype=np.uint8) 

        # Накладываем цветовой фильтр
        thresh = cv2.inRange(hsv_img, h_min, h_max) 
        # Ищем контуры
        _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

        # Создаём прямоугольник из контура с наибольшей площадью
        rect = cv2.minAreaRect( sorted(contours, key = cv2.contourArea, reverse = True)[0] ) 
        rects.append( [color, rect] )

        # Переводим в вершины, округляя координаты
        box = np.int0(cv2.boxPoints(rect)) 
        minX = min(minX, np.ndarray.min( box[...,0] ))
        maxX = max(maxX, np.ndarray.max( box[...,0] ))
        minY = min(minY, np.ndarray.min( box[...,1] ))
        maxY = max(maxY, np.ndarray.max( box[...,1] ))
        
    # Формируем возвращаемый лист
    res = [ [rect[0], [int(rect[1][0][0] - minX), int(rect[1][0][1] - minY)], [int(x) for x in rect[1][1] ], int(rect[1][2])] for rect in rects] 
    # Находим разрешение
    resolution = [maxX - minX, maxY - minY]
    if not(os.path.exists(basedir + '/images/' + room.token + '_map.jpg')):
        room_map = Image.new('RGB', (resolution[0], resolution[1]), (255, 255, 255))
        room_map.save(basedir + '/images/' + room.token + '_map.jpg')

    for i in range(len(res)):
        firstx = int(res[i][1][0] - res[i][2][0]/2)
        lastx = int(res[i][1][0] + res[i][2][0]/2)
        firsty = int(res[i][1][1] - res[i][2][1]/2)
        lasty = int(res[i][1][1] + res[i][2][1]/2)
        room_map = Image.open(basedir + url_for('get_multi', pid=room.token+'_map'))
        draw = ImageDraw.Draw(room_map)
        for x in range(firstx,lastx):
            for y in range(firsty,lasty):
                draw.point((x, y), (res[i][0][2], res[i][0][1], res[i][0][0]))
        room_map.save(basedir + url_for('get_multi', pid=room.token+'_map'))
        res_k = resolution[0] / (lastx - firstx)
        left = - ( (firstx / resolution[0]) * res_k )
        top = - ( (firsty / resolution[1]) * res_k )
        users[i].res_k = res_k
        users[i].top = top
        users[i].left = left
        db.session.commit()        
        
def cur_user():
    if 'Login' in session:
        return User.get(login=session['Login'])
    return None

