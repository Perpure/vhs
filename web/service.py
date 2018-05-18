from web import app, db
from web.helper import read_image, read_video, cur_user, is_true_pixel, read_multi
from web.models import Video, Comment, User, Room, AnonUser
from datetime import datetime

from flask import url_for, redirect, make_response, request, jsonify, session, render_template


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
    if 'anon_id' in session:
        user = AnonUser.query.filter_by(id=session['anon_id']).first()
        action = user.action
        if action == 'calibrate':
            user.action = ''
            db.session.add(user)
            db.session.commit()
            return action
        elif action != '':
            user.action = ''
            db.session.add(user)
            db.session.commit()
            time=datetime.now(tz=None)
            hr=time.hour
            mt=time.minute
            sc=time.second
            ms=round(time.microsecond/1000)
            new=hr*3600000+mt*60000+sc*1000+ms
            old=action[6:]
            action="result"+str(int(old)-new)
            return action
    return ''


@app.route('/askNewComm/<string:vid>', methods=['GET', 'POST'])
def askNewComm(vid):
    video = Video.get(video_id=vid)
    comms=video.comments
    cnt=len(comms)
    return str(cnt)


def getId(Comment):
    return Comment.id


@app.route('/getNewComm/<string:vid>/<int:cont>', methods=['GET', 'POST'])
def getNewComm(vid,cont):
    video = Video.get(video_id=vid)
    comms=video.comments
    sorted(comms,key=getId)
    print(comms)
    result=""
    for i in range(cont,len(comms)):
        result+=str(comms[i].user.login)+",,"+str(comms[i].user.name)+".."+str(comms[i].text)+";;"
    result+=""
    return result


@app.route('/postComm/<string:vid>/<string:text>', methods=['GET', 'POST'])
def postComm(vid,text):
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
        user = AnonUser.query.filter_by(id=session['anon_id']).first()
        if request.method == 'POST':
            width = request.json['width']
            height = request.json['height']
            user.update_resolution(width=width, height=height)
            return jsonify(width=width, height=height)


@app.route('/startSearch/<string:ask>/<int:view>/<int:dat>', methods=['GET', 'POST'])
def startSearch(ask,view,dat):
    sort=""
    if dat:
            sort += "date"
    if view:
            sort += "views"
    if ask!=" ":   
        return render_template('main.html', user=cur_user(), items=Video.get(search=ask,sort=sort))
    
    return render_template('main.html', user=cur_user(), items=Video.get())


@app.route('/showRes/<string:token>', methods=['GET', 'POST'])
def showRes(token):
    room = Room.query.filter_by(token=token).first()  
    time=datetime.now(tz=None)
    hr=time.hour
    mt=time.minute+1
    sc=time.second
    ms=round(time.microsecond/1000)
    for i in range(len(room.color_user.split(';'))):
                ID = room.color_user.split(';')[i].split(',')[0]
                AnonUser.query.filter_by(id=ID).first().action = "result"+str(hr*3600000+mt*60000+sc*1000+ms)
    db.session.commit()
    return 0

