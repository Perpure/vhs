from flask import redirect, render_template, session, url_for, make_response, request, jsonify
from web import app, db
from web.forms import RegForm, LogForm, UploadVideoForm, JoinForm, RoomForm, UploadImageForm, \
    UserProfileForm, AddRoomForm, AddCommentForm
from web.models import User, Video, Room, Color, Comment
from config import basedir
from .helper import read_image, read_video, cur_user, is_true_pixel, read_multi, calibrate_params
from werkzeug.utils import secure_filename
from random import choice
from string import ascii_letters
from werkzeug.exceptions import Aborter
from functools import wraps
from PIL import Image, ImageDraw
from config import ALLOWED_EXTENSIONS
import os

from web import app, db
from web.forms import RegForm, LogForm, UploadVideoForm, JoinForm, RoomForm, UploadImageForm, UserProfileForm, AddCommentForm, AddRoomForm
from web.models import User, Video, Room, Color, Comment
from web.helper import read_image, read_multi, read_video, cur_user, is_true_pixel
from web.video_handler import save_video
from config import basedir

def requiresauth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if cur_user() is None:
            abort = Aborter()
            return abort(403)
        return f(*args, **kwargs)

    return wrapped


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


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html', user=cur_user(), items=Video.get())


@app.route('/viewroom', methods=['GET', 'POST'])
def viewroom():
    user = cur_user()

    if user:
        join_form = JoinForm(csrf_enabled=False)
        user.Action = ""
        db.session.commit()
        add_room_form = AddRoomForm(csrf_enabled=False)
        if add_room_form.validate_on_submit():
            token = add_room_form.token.data
            room = Room(token=token, capitan_id=user.id)
            for i in range(1, 7):
                room.Color.append(Color.query.filter_by(id=str(i)).first())
                room.color_user = str(user.id) + ',1'
            db.session.add(room)
            db.session.commit()
            user.rooms.append(room)
            db.session.commit()
            return redirect(url_for('addroom',  token=add_room_form.token.data))


        if join_form.validate_on_submit():
            if Room.query.filter_by(token=str(join_form.token.data)):
                return redirect(url_for('room', token=join_form.token.data))
        rooms = user.rooms
    else:
        return redirect(url_for('log'))
    return render_template('viewroom.html', user=cur_user(), join_form=join_form,add_room_form=add_room_form, rooms=rooms)


@app.route('/addroom/<string:token>', methods=['GET', 'POST'])
def addroom(token):
    user = cur_user()
    if user:
        pass
    else:
        return redirect(url_for('log'))

    return render_template('addroom.html', user=cur_user(), token=token)


@app.route('/room/<string:token>', methods=['GET', 'POST'])
def room(token):
    user = cur_user()
    Room_Form = RoomForm()
    calibrate_url = None
    result_url = None

    if user:
        room = Room.query.filter_by(token=token).first()

        if Room_Form.validate_on_submit():
            for i in range(len(room.color_user.split(';'))):
                ID = room.color_user.split(';')[i].split(',')[0]
                User.query.filter_by(id=ID).first().Action = "calibrate"
            db.session.commit()

        if not ((room in user.rooms) and (room in user.room_capitan)):
            user.rooms.append(room)
            if room.color_user:
                color_id = len(room.color_user.split(';')) + 1
                room.color_user += ';' + str(user.id) + ',' + str(color_id)
            else:
                room.color_user = str(user.id) + ',1'
            db.session.commit()

        if room.color_user is not None:
            colors = room.color_user.split(';')
            for i in range(len(colors)):
                if colors[i].split(',')[0] == str(user.id):
                    color = Color.query.filter_by(id=colors[i].split(',')[1]).first().color
                    calibrate_url = url_for('calibrate', color=color)
                    result_url = url_for('result', token=token, color=color)
                    break
        users = room.user

        image_form = UploadImageForm(csrf_enabled=False)
        if image_form.validate_on_submit():
            if 'image' not in request.files:
                return render_template('room.html', room=room, user=cur_user(),
                                       calibrate_url=calibrate_url, users=users,
                                       image_form=UploadImageForm(csrf_enabled=False),
                                       result_url=result_url, Room_Form=Room_Form, loaded=False)

            file = request.files['image']
            if file.filename == '':
                return render_template('room.html', room=room, user=cur_user(),
                                       calibrate_url=calibrate_url, users=users,
                                       image_form=UploadImageForm(csrf_enabled=False),
                                       result_url=result_url, Room_Form=Room_Form, loaded=False)

            if file and allowed_file(file.filename):
                file.save(basedir + '/images/' + room.token + '.' + file.filename.split('.')[-1].lower())
                return render_template('room.html', room=room, user=cur_user(),
                                       calibrate_url=calibrate_url, users=users,
                                       image_form=image_form, result_url=result_url,
                                       Room_Form=Room_Form, loaded=True)

    else:
        return redirect(url_for('log'))
    return render_template('room.html', room=room, user=cur_user(),
                           calibrate_url=calibrate_url, users=users,
                           image_form=image_form, result_url=result_url, Room_Form=Room_Form, loaded=False)


def allowed_file(filename):
    return ('.' in filename and
            filename.split('.')[-1].lower() in app.config["ALLOWED_EXTENSIONS"])


@app.route('/calibrate/<string:color>', methods=['GET', 'POST'])
def calibrate(color):
    user = cur_user()
    user.Action = ""
    db.session.commit()
    return render_template('color.html', color=color)


@app.route('/upload', methods=['GET', 'POST'])
@requiresauth
def upload():
    """
    Отвечает за вывод страницы загрузки и загрузку файлов
    :return: Страница загрузки
    """
    form = UploadVideoForm(csrf_enabled=False)
    error = ""

    if form.validate_on_submit():
        try:
            if 'video' not in request.files:
                return redirect(request.url)

            file = request.files['video']

            if file.filename == '':
                return redirect(request.url)

            if form.geotag_data.data != "":
                coords = form.geotag_data.data.split(',')
            else:
                coords = None

            if file and allowed_file(file.filename):
                save_video(file, form.title.data)

                return redirect(request.url)
        except:
            error = "Произошла ошибка при загрузке видео. Пожалуйста, повторите попытку"
        finally:
            return redirect(url_for("main"))

    return render_template('upload_video.html', form=form, user=cur_user(), error=error, formats = ALLOWED_EXTENSIONS)


@app.route('/result/<string:token>/<string:color>', methods=['GET', 'POST'])
def result(token, color):
    room = Room.query.filter_by(token=token).first()
    user = cur_user()
    colors = room.color_user.split(';')
    for i in range(len(colors)):
        if colors[i].split(',')[0] == str(user.id):
            color = Color.query.filter_by(id=colors[i].split(',')[1]).first().color
            break
    rezolutionx = 400
    rezolutiony = 887
    sourcex = 800
    sourcey = 600
    R = int(color[1:3], 16)
    G = int(color[3:5], 16)
    B = int(color[5:7], 16)
    print(basedir)
    image = Image.open(basedir + url_for('get_multi', pid=token))
    width = image.size[0]
    height = image.size[1]
    firstx = 0
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
                    firstx = i
                    firsty = j
                if lastx < i:
                    lastx = i
                if lasty < j:
                    lasty = j
    w, h = calibrate_params(firstx, firsty, lastx, lasty, rezolutionx, rezolutiony)
    k = int((width/w)/(sourcex/rezolutionx)*100)
    return render_template('rezult.html', pid='1', top=-(firsty/height)*sourcey, left=-(firstx/width)*sourcex, width=k)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    """
    Отвечает за вывод страницы регистрации и регистрацию
    :return: Страница регистрации
    """
    form = RegForm()

    if form.validate_on_submit():
        user = User(form.login_reg.data)
        user.save(form.password_reg.data)
        session["Login"] = user.login
        return redirect(url_for("main"))

    return render_template('reg.html', form=form, user=cur_user())


@app.route('/auth', methods=['GET', 'POST'])
def log():
    """
    Отвечает за вывод страницы входа и вход
    :return: Страница входа
    """
    form = LogForm()

    if form.validate_on_submit():
        session["Login"] = form.login_log.data
        return redirect(url_for("main"))

    return render_template('auth.html', form=form, user=cur_user())


@app.route('/cabinet', methods=['GET', 'POST'])
@requiresauth
def cabinet():
    """
    Отвечает за вывод страницы личного кабинета
    :return: Страница личного кабинета
    """

    video_list = Video.get()
    items = []
    user = cur_user()
    for item in video_list:
        if item.user == user.id:
            items.append(item)

    form = UserProfileForm()
    if form.validate_on_submit():
        user = cur_user()
        if form.change_name.data:
            user.change_name(form.change_name.data)
        if form.change_password.data:
            user.save(form.change_password.data)
        if form.channel_info.data:
            user.change_channel_info(form.channel_info.data)
        return redirect(url_for("cabinet"))
    return render_template('cabinet.html', form=form, user=cur_user(), items=items)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'Login' in session:
        session.pop('Login')
    return redirect('/')


@app.route('/video/<string:vid>/video.mp4')
def get_video(vid):
    video_binary = read_video(vid)
    response = make_response(video_binary)
    response.headers.set('Content-Type', 'video/mp4')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='video/%s/video.mp4' % vid)
    return response


@app.route('/tellRes', methods=['GET', 'POST'])
def tellRes():
    if cur_user():
        user = cur_user()
        if request.method == 'POST':
            width = request.json['width']
            height = request.json['height']
            user.update_resolution(width=width, height=height)
            return jsonify(width=width, height=height)

@app.route('/askAct', methods=['GET', 'POST'])
def askAct():
    action = ""
    if cur_user():
        user = cur_user()
        action = user.Action
    return action


@app.route('/play/<string:vid>', methods=['GET', 'POST'])
def play(vid):
    video = Video.get(video_id=vid)
    if not video:
        abort = Aborter() 
        return abort(404)

    user = cur_user()
    form = AddCommentForm()

    if user and user not in video.viewers:
        video.add_viewer(user)
    
    if form.validate_on_submit():
        comment = Comment(form.message.data, video.id, user.id)
        comment.save()

    return render_template('play.html', user=user, vid=vid, video=video, form=form)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
