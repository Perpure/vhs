# coding=utf-8
from datetime import datetime
from flask import url_for, redirect, make_response, request, jsonify, session, render_template
from web import app, db
from web.helper import read_image, read_video, cur_user, read_multi
from web.models import Video, Comment, Room, AnonUser, User


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


@app.route('/video/data', methods=['GET'])
def get_video_data_search():
    search = request.args.get('search')
    videos = Video.get(search=search)

    return jsonify([{"title": video.title,
                     "link": url_for("play", vid=video.id),
                     "preview": url_for("get_image", pid=video.id),
                     "geotags": [(gt.longitude, gt.latitude) for gt in video.geotags]} for video in videos])


@app.route('/askAct/<int:room_id>', methods=['GET', 'POST'])
def askAct(room_id):
    if 'anon_id' in session:
        room = Room.query.get(room_id)
        user = AnonUser.query.get(session['anon_id'])
        action = user.action
        if action == 'calibrate':
            user.action = ''
            db.session.add(user)
            db.session.commit()
            return jsonify({"action": action,
                            "color": user.color})
        elif action == 'result' or action == 'resultS':
            noSound = True
            if action == 'resultS':
                noSound = False
            user.action = ''
            db.session.add(user)
            db.session.commit()
            time = datetime.now(tz=None)
            hr = time.hour
            mt = time.minute
            sc = time.second
            ms = round(time.microsecond/1000)
            new = hr * 3600000 + mt * 60000 + sc * 1000 + ms
            action = "result"
            old = user.time
            time = str(old-new)
            return jsonify({"action": action,
                            "time": time,
                            "top": user.top,
                            "left": user.left,
                            "width": user.res_k,
                            "noSound": noSound})
        elif action == 'refresh':
            user.action = ''
            db.session.add(user)
            db.session.commit()
            return jsonify({"action": action})
        elif action == 'update':
            user.action = ''
            db.session.add(user)
            db.session.commit()
            users = room.get_devices()
            return jsonify({"action": action, "count": len(users)+1})
    return jsonify({"action": ''})


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


@app.route('/tellRes', methods=['GET', 'POST'])
def tellRes():
    if 'anon_id' in session:
        user = AnonUser.query.get(session['anon_id'])
        if request.method == 'POST':
            width = request.json['width']
            height = request.json['height']
            user.update_resolution(width=width, height=height)
            return jsonify(width=width, height=height)


@app.route('/startSearch', methods=['GET'])
def startSearch():
    sort = ""
    ask = request.args.get('ask')
    view = request.args.get('view')
    dat = request.args.get('dat')

    if dat:
        sort += "date"
    if view:
        sort += "views"
    if ask != " ":
        return render_template('main.html', user=cur_user(), items=Video.get(search=ask, sort=sort))

    return render_template('main.html', user=cur_user(), items=Video.get())


@app.route('/showRes/<int:room_id>', methods=['GET', 'POST'])
def showRes(room_id):
    room = Room.query.get(room_id)
    users = room.get_devices()
    time = datetime.now(tz=None)
    hr = time.hour
    mt = time.minute
    sc = time.second
    ms = round(time.microsecond / 1000)
    zero = hr * 3600000 + mt * 60000 + sc * 1000 + ms
    for member in users:
        time = datetime.now(tz=None)
        hr = time.hour
        mt = time.minute
        sc = time.second
        ms = round(time.microsecond / 1000)
        now = hr * 3600000 + mt * 60000 + sc * 1000 + ms
        now += 15000 - (now-zero)
        member.action = "result"
        member.time = now
    users[0].action = "resultS"
    db.session.commit()
    return ""

@app.route('/subscribe/<int:ID>', methods=['GET', 'POST'])
def subscribe(ID):
    user = cur_user()
    blog=User.get(id=ID)
    if user in blog.subscribers:
        blog.subscribers.remove(user)
        db.session.add(user)
        db.session.commit()
    else:
        user.follow(blog)
    
    return "nice"