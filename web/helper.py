from config import basedir
from web import db, app
from web.models import User
from PIL import Image, ImageDraw, ImageEnhance
from web.models import User
from web import app
from functools import wraps
from flask import session, redirect, url_for


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


def count_params(room, color, user):
    rezolutionx = user.device_width
    rezolutiony = user.device_height
    source = Image.open(basedir + url_for('get_multi', pid=1))
    sourcex = source.size[0]
    sourcey = source.size[1]
    R = int(color[1:3], 16)
    G = int(color[3:5], 16)
    B = int(color[5:7], 16)
    image = Image.open(basedir + url_for('get_multi', pid=room.token))
    converter = ImageEnhance.Color(image)
    image = converter.enhance(2)
    width = image.size[0]
    height = image.size[1]
    firstx = 0
    firsty = 0
    lasty = 0
    lastx = 0
    pix = image.load()
    for i in range(width):
        for j in range(height):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]
            if is_true_pixel(r,g,b,R,G,B):
                if not (firstx):
                    try:
                        for f in range(-20,-15):
                            if is_true_pixel(pix[i-f, j-f][0],pix[i-f, j-f][1],pix[i-f, j-f][2],R,G,B):
                                firstx = i
                                firsty = j
                                break
                    except:
                        pass
                if firstx > i:
                    try:
                        for f in range(-20,-15):
                            if is_true_pixel(pix[i-f, j-f][0],pix[i-f, j-f][1],pix[i-f, j-f][2],R,G,B):
                                firstx = i
                                break
                    except:
                        pass
                if firsty > j:
                    try:
                        for f in range(-20,-15):
                            if is_true_pixel(pix[i-f, j-f][0],pix[i-f, j-f][1],pix[i-f, j-f][2],R,G,B):
                                firsty = j
                                break
                    except:
                        pass
                if lastx < i:
                    try:
                        for f in range(15,20):
                            if is_true_pixel(pix[i-f, j-f][0],pix[i-f, j-f][1],pix[i-f, j-f][2],R,G,B):
                                lastx = i
                                break
                    except:
                        pass
                if lasty < j:
                    try:
                        for f in range(15,20):
                            if is_true_pixel(pix[i-f, j-f][0],pix[i-f, j-f][1],pix[i-f, j-f][2],R,G,B):
                                lasty = j
                                break
                    except:
                        pass
    w = lastx-firstx
    user.color = color
    user.res_k = int((width/w)/(sourcex/rezolutionx)*100)
    user.top = -(firsty/height)*sourcey
    user.left = -(firstx/width)*sourcex
    db.session.commit()
    room_map = Image.open(basedir + url_for('get_multi', pid=room.token+'_map'))
    draw = ImageDraw.Draw(room_map)
    for i in range(firstx,lastx):
        for j in range(firsty,lasty):
            draw.point((i, j), (R,G,B))
    room_map.save(basedir + '/images/' + room.token + '_map.jpg')


def cur_user():
    if 'Login' in session:
        return User.get(login=session['Login'])
    return None

