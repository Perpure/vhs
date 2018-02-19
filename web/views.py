from flask import redirect, render_template, make_response
from web import app
import os
from config import basedir

def read_image(pid):
    path=basedir + '/images/%s.jpg' % pid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b

@app.route('/images/<int:pid>.jpg')
def get_image(pid):
    image_binary = read_image(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/calibrate', methods=['GET', 'POST'])
def multicheck():
    return render_template('color.html', color="#FF0000")

@app.route('/rezult', methods=['GET', 'POST'])
def rezult():
    return render_template('rezult.html', pid=1)
