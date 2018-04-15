from config import basedir
from flask import session
from web.models import User


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
    return (r in range(R-50, R+50))and(g in range(G-50, G+50))and(b in range(B-50, B+50))


def calibrate_params(firstx, firsty, lastx, lasty, rezolutionx, rezolutiony):
    x = lastx - firstx + 1
    y = lasty - firsty + 1
    if (x / y) > (rezolutionx / rezolutiony):
        e = (x / y) - (rezolutionx / rezolutiony)
        w = x
        h = y
        w1 = 0
        h1 = 0
        while True:
            w -= 1
            if (w / h) <= (rezolutionx / rezolutiony):
                if (rezolutionx / rezolutiony) - (w / h) < ((w + 1) / h) - (rezolutionx / rezolutiony):
                    e = (rezolutionx / rezolutiony) - (w / h)
                    w1 = w
                    h1 = h
                    break
                else:
                    e = (rezolutionx / rezolutiony) - ((w + 1) / h)
                    w1 = w + 1
                    h1 = h
                    break
        w = x
        h = y
        while True:
            h += 1
            if (w / h) <= (rezolutionx / rezolutiony):
                if (rezolutionx / rezolutiony) - (w / h) < (w / (h - 1)) - (rezolutionx / rezolutiony):
                    if ((rezolutionx / rezolutiony) - (w / h)) < e:
                        w1 = w
                        h1 = h
                    break
                else:
                    if ((rezolutionx / rezolutiony) - (w / (h - 1))) < e:
                        w1 = w
                        h1 = h - 1
                    break
    else:
        e = (rezolutionx / rezolutiony) - (x / y)
        w = x
        h = y
        w1 = 0
        h1 = 0
        while True:
            w += 1
            if (w / h) <= (rezolutionx / rezolutiony):
                if (rezolutionx / rezolutiony) - (w / h) < ((w - 1) / h) - (rezolutionx / rezolutiony):
                    e = (rezolutionx / rezolutiony) - (w / h)
                    w1 = w
                    h1 = h
                    break
                else:
                    e = (rezolutionx / rezolutiony) - ((w - 1) / h)
                    w1 = w - 1
                    h1 = h
                    break
        w = x
        h = y
        while True:
            h -= 1
            if (w / h) <= (rezolutionx / rezolutiony):
                if (rezolutionx / rezolutiony) - (w / h) < (w / (h + 1)) - (rezolutionx / rezolutiony):
                    if ((rezolutionx / rezolutiony) - (w / h)) < e:
                        w1 = w
                        h1 = h
                    break
                else:
                    if ((rezolutionx / rezolutiony) - (w / (h + 1))) < e:
                        w1 = w
                        h1 = h + 1
                    break
    return w1, h1


def cur_user():
    if 'Login' in session:
        return User.get(login=session['Login'])
    return None

