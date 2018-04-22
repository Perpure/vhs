from web import app, db
from web.helper import read_image, read_video, cur_user, is_true_pixel, read_multi, calibrate_params
from web.models import Video

from flask import url_for, redirect, make_response, request, jsonify, session

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'Login' in session:
        session.pop('Login')
    return redirect('/')


@app.route('/images/<string:pid>.jpg')
def get_multi(pid):
    image_binary = read_multi(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response


@app.route('/images/<string:pid>/preview.png')
def get_image(pid):
    image_binary = read_image(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response

@app.route('/video/<string:vid>/video.mp4')
def get_video(vid):
    video_binary = read_video(vid)
    response = make_response(video_binary)
    response.headers.set('Content-Type', 'video/mp4')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='video/%s/video.mp4' % vid)
    return response

@app.route('/video/data')
def get_video_data():
    videos = Video.get()

    return jsonify([{"title" : video.title,
                     "link" : url_for("play", vid=video.id),
                     "preview" : url_for("get_image", pid=video.id),
                     "geotags" : [(gt.longitude , gt.latitude) for gt in video.geotags]} for video in videos])

@app.route('/video/data/<string:search>')
def get_video_data_search(search):
    videos = Video.get(search=search)

    return jsonify([{"title" : video.title,
                     "link" : url_for("play", vid=video.id),
                     "preview" : url_for("get_image", pid=video.id),
                     "geotags" : [(gt.longitude , gt.latitude) for gt in video.geotags]} for video in videos])
    

@app.route('/askAct', methods=['GET', 'POST'])
def askAct():
    action = ""
    if cur_user():
        user = cur_user()
        action = user.action
    return action


@app.route('/tellRes', methods=['GET', 'POST'])
def tellRes():
    if cur_user():
        user = cur_user()
        if request.method == 'POST':
            width = request.json['width']
            height = request.json['height']
            user.update_resolution(width=width, height=height)
            return jsonify(width=width, height=height)
