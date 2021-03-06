# coding=utf-8
import mimetypes
import os
import re
import textwrap
import json
from datetime import datetime
from flask import url_for, redirect, make_response, request, jsonify, session, render_template, Response, abort
from web import app, db
from web.helper import read_image, cur_user, read_multi, decode_iso8601_duration
from web.models import Video, Comment, Room, Device, User
from config import basedir, BUFF_SIZE, GOOGLE_API_KEY
from flask.json import dumps
import requests


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


def partial_response(path, start, end=None):
    file_size = os.path.getsize(path)

    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1, start + BUFF_SIZE - 1)
    length = end - start + 1

    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(bytes, 206, mimetype=mimetypes.guess_type(path)[0], direct_passthrough=True)
    response.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, end, file_size))
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def get_bounds_of_header_range(range):
    m = re.match(r'bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None


@app.route('/video/<string:vid>/video.mp4')
def get_video(vid):
    path = app.config['VIDEO_SAVE_PATH'] + '/%s/video.mp4' % vid
    print(path)
    range = request.headers.get('Range')
    start, end = get_bounds_of_header_range(range)
    return partial_response(path, start, end)


@app.route('/askNewComm/<string:vid>', methods=['GET', 'POST'])
def askNewComm(vid):
    video = Video.get(video_id=vid)
    return str(len(video.comments))


@app.route('/getNewComm/<string:vid>/<int:cont>', methods=['GET', 'POST'])
def getNewComm(vid, cont):
    comms = Video.get(video_id=vid).comments
    comms.sort(key=lambda x: x.id)
    result = []
    for i in range(cont, len(comms)):
        result.append({"login": comms[i].user.login, "name": comms[i].user.name, "text": comms[i].text,
                       "ava": comms[i].user.avatar_url()})
    return jsonify(result)


@app.route('/postComm/<string:vid>/', methods=['GET'])
def postComm(vid):
    text = request.args.get('comm')
    video = Video.get(video_id=vid)
    user = cur_user()
    if len(text) <= 1000:
        comment = Comment(text, video.id, user.id)
        comment.save()
    return "lol"


@app.route('/likeVideo/<string:vid>/', methods=['GET', 'POST'])
def likeVideo(vid):
    user = cur_user()
    video = Video.get(video_id=vid)

    if user:
        if user in video.likes:
            video.likes.remove(user)
            db.session.add(user)
            db.session.commit()
        else:
            video.add_like(user)
            if user in video.dislikes:
                video.dislikes.remove(user)
                db.session.add(user)
                db.session.commit()
    return jsonify([{"likes": str(len(video.likes)),
                     "dislikes": str(len(video.dislikes))}])


@app.route('/dislikeVideo/<string:vid>/', methods=['GET', 'POST'])
def dislikeVideo(vid):
    user = cur_user()
    video = Video.get(video_id=vid)

    if user:
        if user in video.dislikes:
            video.dislikes.remove(user)
            db.session.add(user)
            db.session.commit()
        else:
            video.add_dislike(user)
            if user in video.likes:
                video.likes.remove(user)
                db.session.add(user)
                db.session.commit()
    return jsonify([{"likes": str(len(video.likes)),
                     "dislikes": str(len(video.dislikes))}])


@app.route('/tellRes', methods=['POST'])
def tellRes():
    if 'anon_id' in session:
        user = Device.query.get(session['anon_id'])
        if request.method == 'POST':
            width = request.form['width']
            height = request.form['height']
            user.update_resolution(width=width, height=height)
            return '0'


@app.route('/subscribe/<int:ID>', methods=['GET', 'POST'])
def subscribe(ID):
    user = cur_user()
    blog = User.get(id=ID)
    if user in blog.subscribers:
        blog.subscribers.remove(user)
        db.session.add(user)
        db.session.commit()
    else:
        user.follow(blog)

    return "nice"


@app.route('/youtube_videos')
def videos_from_youtube():
    query = request.args.get('query')
    params = {
        'q': query,
        'key': GOOGLE_API_KEY,
        'part': 'id',
        'type': 'video',
        'maxResults': 20
    }

    if request.args.get('nextPageToken') is not None:
        params.update({'pageToken': request.args.get('nextPageToken')})

    search_res = requests.get('https://www.googleapis.com/youtube/v3/search', params).json()
    if search_res.get('error') is not None:
        return abort(500)

    ids = ''
    for item in search_res['items']:
        ids += item['id']['videoId'] + ','
    if ids == '':
        return abort(404)
    videos_data = requests.get('https://www.googleapis.com/youtube/v3/videos', {
        'id': ids,
        'part': 'snippet,contentDetails',
        'key': GOOGLE_API_KEY
    }).json()

    response = {}
    response.update({'nextPageToken': search_res.get('nextPageToken', 0)})
    videos = []
    for data in videos_data['items']:
        snippet = data.get('snippet')
        duration = decode_iso8601_duration(data.get('contentDetails').get('duration'))
        video = {
            'title': textwrap.shorten(snippet.get('title'), width=25, placeholder='...'),
            'preview': snippet.get('thumbnails').get('medium').get('url'),
            'author': textwrap.shorten(snippet.get('channelTitle'), width=20, placeholder='...'),
            'duration': duration,
            'id': data.get('id')
        }
        videos.append(video)

    response.update({'videos': videos})

    return jsonify(response)


@app.route('/search_videos', methods=['POST'])
def search_for_videos():
    search = request.form['search']
    date = request.form['date']
    name = request.form['name']
    geo = request.form['geo_need']

    tags = []
    search = search.strip()
    elements = search.split(' ')
    for el in elements:
        if el[0] == '#':
            search = search.replace(el, "")
            tags.append(el)
    search = search.strip()
    video_pack = Video.get(search, tags, date, name, geo)
    jsoned = []
    jsoned.append(json.dumps([video.serialize('ext') for video in video_pack[0]]))
    jsoned.append(json.dumps([video.serialize() for video in video_pack[1]]))
    return json.dumps(jsoned)


@app.route('/change_youtube_state/<int:ID>', methods=['GET', 'POST'])
def change_youtube_state(ID):
    room = Room.query.get(ID)
    room.is_playing_youtube = not room.is_playing_youtube
    db.session.commit()
    return "nice"
