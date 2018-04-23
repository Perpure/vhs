from config import basedir
from web import db, app
from web.models import User
from PIL import Image, ImageDraw
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
    return (r in range(R-75, R+75))and(g in range(G-75, G+75))and(b in range(B-75, B+75))


def count_params(room, color, user):
    rezolutionx = 400
    rezolutiony = 887
    source = Image.open(basedir + url_for('get_multi', pid=1))
    sourcex = source.size[0]
    sourcey = source.size[1]
    R = int(color[1:3], 16)
    G = int(color[3:5], 16)
    B = int(color[5:7], 16)
    image = Image.open(basedir + url_for('get_multi', pid=room.token))
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
                        for f in range(-20,-5):
                            if is_true_pixel(pix[i-f, j-f][0],pix[i-f, j-f][1],pix[i-f, j-f][2],R,G,B):
                                firstx = i
                                firsty = j
                    except:
                        pass
                if lastx < i:
                    try:
                        for f in range(5,20):
                            if is_true_pixel(pix[i-f, j-f][0],pix[i-f, j-f][1],pix[i-f, j-f][2],R,G,B):
                                lastx = i
                    except:
                        pass
                if lasty < j:
                    try:
                        for f in range(5,20):
                            if is_true_pixel(pix[i-f, j-f][0],pix[i-f, j-f][1],pix[i-f, j-f][2],R,G,B):
                                lasty = j
                    except:
                        pass
    w = lastx-firstx
    user.color = color

    k = int((width / w) / (sourcex / rezolutionx) * 100)
    user.res_k = k
    user.top = -(firsty / height) * sourcey * k / 100
    user.left = -(firstx / width) * sourcex * k / 100
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

