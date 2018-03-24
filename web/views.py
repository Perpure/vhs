from flask import redirect, render_template, session, url_for, make_response, request
from web import app, db
from web.forms import RegForm, LogForm, UploadVideoForm, JoinForm, UploadImageForm, UserProfileForm
from web.models import User, Video, Room, Color
from config import basedir
from .helper import read_image, read_video, cur_user, IsVideoViewed, is_true_pixel
from werkzeug.utils import secure_filename
from random import choice
from string import ascii_letters
from werkzeug.exceptions import Aborter
from functools import wraps
from web.video_handler import save_video
from PIL import Image, ImageDraw
import os

def requiresauth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if cur_user() is None:
            abort = Aborter()
            return abort(403)
        return f(*args, **kwargs)
    return wrapped


@app.route('/images/<string:pid>.jpg')
def get_image(pid):
    image_binary = read_image(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html', user=cur_user())


@app.route('/viewroom', methods=['GET', 'POST'])
def viewroom():
    user=cur_user()
    if user:
        form = JoinForm(csrf_enabled=False)
        if form.validate_on_submit():
            if Room.query.filter_by(token=str(form.token.data)):
                return redirect(url_for('room', token=form.token.data))
        rooms = user.Room.all()
    else:
        return redirect(url_for('log'))
    return render_template('viewroom.html', user=cur_user(), form=form, rooms = rooms)


@app.route('/addroom', methods=['GET', 'POST'])
def addroom():
    user=cur_user()
    if user:
        token=''.join(choice(ascii_letters) for i in range(24))
        room=Room(token=token)
        for i in range(1,7):
            room.Color.append(Color.query.filter_by(id=str(i)).first())
        db.session.add(room)
        db.session.commit()
        user.Room.append(room)
        room.color_user = str(user.id) + ',1'
        db.session.commit()
    else:
        return redirect(url_for('log'))
    return render_template('addroom.html', user=cur_user(), token=token)


@app.route('/room/<string:token>', methods=['GET', 'POST'])
def room(token):
    user=cur_user()
    if user:
        room = Room.query.filter_by(token=token).first()
        if not(room in user.Room):
            user.Room.append(room)
            if room.color_user:
                color_id = len(room.color_user.split(';')) + 1
                room.color_user += ';' + str(user.id) + ',' + str(color_id)
            else:
                room.color_user = str(user.id) + ',1'
            db.session.commit()
        colors=room.color_user.split(';')
        for i in range(len(colors)):
            if colors[i].split(',')[0] == str(user.id):
                color = Color.query.filter_by(id=colors[i].split(',')[1]).first().color
                calibrate_url = url_for('calibrate', color=color)
                result_url = url_for('result', token=token, color=color)
                break
        users=room.User

        image_form = UploadImageForm(csrf_enabled=False)
        if image_form.validate_on_submit():
            if 'image' not in request.files:
                return render_template('room.html', user=cur_user(), calibrate_url=calibrate_url, users=users,
                                       image_form=UploadImageForm(csrf_enabled=False), result_url=result_url)

            file = request.files['image']
            if file.filename == '':
                return render_template('room.html', user=cur_user(), calibrate_url=calibrate_url, users=users,
                                       image_form=UploadImageForm(csrf_enabled=False), result_url=result_url)
    
            if file and allowed_file(file.filename):
                file.save(basedir+'/images/'+room.token+'.'+file.filename.split('.')[-1].lower())
                return render_template('room.html', user=cur_user(), calibrate_url=calibrate_url, users=users,
                                       image_form=image_form, result_url=result_url)

    else:
        return redirect(url_for('log'))
    return render_template('room.html', user=cur_user(), calibrate_url=calibrate_url, users=users,
                           image_form=image_form, result_url=result_url)
    
def allowed_file(filename):
    return ('.' in filename and
            filename.split('.')[-1].lower() in app.config["ALLOWED_EXTENSIONS"])


@app.route('/calibrate/<string:color>', methods=['GET', 'POST'])
def calibrate(color):
    return render_template('color.html', color=color)


@app.route('/upload', methods=['GET', 'POST'])
@requiresauth
def upload():
    """
    Отвечает за вывод страницы загрузки и загрузку файлов
    :return: Страница загрузки
    """
    form = UploadVideoForm(csrf_enabled=False)

    if form.validate_on_submit():
        if 'video' not in request.files:
            return redirect(request.url)

        file = request.files['video']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            save_video(file, form.title.data)

            return redirect(request.url)

    return render_template('upload_video.html', form=form, user=cur_user())


@app.route('/result/<string:token>/<string:color>', methods=['GET', 'POST'])
def result(token,color):
    room = Room.query.filter_by(token=token).first()
    user=cur_user()
    colors=room.color_user.split(';')
    for i in range(len(colors)):
        if colors[i].split(',')[0] == str(user.id):
            color=Color.query.filter_by(id=colors[i].split(',')[1]).first().color
            break
    sourcex=800
    sourcey=600
    R = int(color[1:3],16)
    G = int(color[3:5],16)
    B = int(color[5:7],16)
    print(basedir)
    image = Image.open(basedir+url_for('get_image', pid=token))
    width = image.size[0]
    height = image.size[1]	
    pix = image.load()
    for i in range(width):
        for j in range(height):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]
            if (is_true_pixel(r,g,b,R,G,B)):
                return render_template('rezult.html', pid='1', top=-(j/height)*sourcey, left=-(i/width)*sourcex)

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
    form = UserProfileForm()
    print("start")
    if form.validate_on_submit():
        print("validate")
        user = cur_user()
        if form.change_name.data:
            user.change_name(form.change_name.data)
        if form.change_password.data:
            user.save(form.change_password.data)
        if form.channel_info.data:
            user.change_channel_info(form.channel_info.data)
        return redirect(url_for("cabinet"))
    print("end")
    return render_template('cabinet.html', form=form, user=cur_user())


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'Login' in session:
        session.pop('Login')
        IsVideoViewed.is_viewed = []
    return redirect('/')


@app.route('/video/<string:vid>/video.mp4')
def get_video(vid):
    video_binary = read_video(vid)
    response = make_response(video_binary)
    response.headers.set('Content-Type', 'video/mp4')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='video/%s/video.mp4' % vid)
    return response


@app.route('/play/<string:vid>', methods=['GET', 'POST'])
def play(vid):
    video = Video.get(vid)
    user = cur_user()
    is_viewed = IsVideoViewed.is_viewed
    if (video.id not in is_viewed) and (video is not None) and (user is not None):
        IsVideoViewed.is_viewed.append(video.id)
        video.views += 1
        db.session.add(video)
        db.session.commit()
    return render_template('play.html', user=cur_user(), vid=vid, video=Video.get(vid), video_views=video.views)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
