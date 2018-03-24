from config import basedir
def read_image(pid):
    path=basedir + '/images/%s.jpg' % pid
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
