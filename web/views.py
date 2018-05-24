from web import app, db
from web.forms import RegForm, LogForm, UploadVideoForm, JoinForm, RoomForm, UploadImageForm, \
    UserProfileForm, AddRoomForm, SearchingVideoForm, VideoToRoomForm
from web.models import User, Video, Room, Color, Comment, Geotag, Tag, AnonUser, RoomDeviceColorConnector
from web.helper import read_image, read_video, allowed_image, allowed_file, cur_user, is_true_pixel, \
    read_multi, parse, requiresauth, anon_user, image_loaded
from web.video_handler import save_video
from wtforms.validators import ValidationError
from config import basedir, ALLOWED_EXTENSIONS
from flask import redirect, render_template, session, url_for, make_response, request, jsonify
from flask.json import JSONDecoder, dumps
from werkzeug.utils import secure_filename
from random import choice
from string import ascii_letters
from werkzeug.exceptions import Aborter
from PIL import Image, ImageDraw
import os
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html', user=cur_user(), items=Video.get())

@app.route('/createroom', methods=['GET', 'POST'])
def createroom():
    user = anon_user()
    user.action = ""
    db.session.commit()

    add_room_form = AddRoomForm(csrf_enabled=False, prefix="Submit_Add")

    if add_room_form.validate_on_submit():
        token = add_room_form.token.data
        room = Room(token=token, capitan_id=user.id)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('room', token=add_room_form.token.data))
    return render_template('create_room.html', add_room_form=add_room_form)

@app.route('/viewroom', methods=['GET', 'POST'])
def viewroom():
    user = anon_user()
    join_form = JoinForm(csrf_enabled=False, prefix="Submit_Join")
    user.action = ""
    db.session.commit()

    if join_form.validate_on_submit():
        if Room.get(token=str(join_form.token.data)):
            return redirect(url_for('room', token=join_form.token.data))
    return render_template('viewroom.html', user=cur_user(), join_form=join_form,
                           rooms=Room.get(), anon=user)



@app.route('/room/<string:token>', methods=['GET', 'POST'])
def room(token):
    user = anon_user()
    Room_Form = RoomForm()
    room = Room.query.filter_by(token=token).first()
    if room:
        room_map_url = token + '_map'
        raw_user_rooms = RoomDeviceColorConnector.query.filter_by(anon=user)
        user_rooms = [rac.room for rac in raw_user_rooms]
        users = room.get_devices()

        if (not(room in user_rooms)) and (room.captain != user):
            color_id = len(users) + 1
            if color_id > 6:
                return redirect(url_for('viewroom'))
            col = Color.query.get(color_id)
            rac = RoomDeviceColorConnector(anon=user, room=room, color=col)
            db.session.add(rac)
            db.session.commit()

        users = room.get_devices()

        if Room_Form.validate_on_submit():
            for member in users:
                member.action = "calibrate"
            db.session.commit()

        for member in users:
            rac = RoomDeviceColorConnector.query.filter_by(room=room,
                                                           anon=member).first()
            member.color = rac.color.color
            db.session.commit()

        image_form = UploadImageForm(csrf_enabled=False)
        if image_form.validate_on_submit():
            return image_loaded(request, room, user, users, UploadImageForm(csrf_enabled=False), image_form, Room_Form)
        return render_template('room.html', room=room, user=cur_user(), color=user.color, users=users, count=len(users)+1,
                               image_form=image_form, Room_Form=Room_Form, loaded=False, anon=user,
                               room_map=room_map_url, map_ex=os.path.exists(basedir + '/images/' + room.token + '_map.jpg'))
    else:
        return redirect(url_for('viewroom'))
    
@app.route('/room/<string:token>/choose_video/<string:vid_id>', methods=['GET', 'POST'])
def choosed_video(token,vid_id):
    user = anon_user()
    room = Room.query.filter_by(token=token).first()
    vid = Video.query.get(vid_id)
    if vid and room:
        users = room.get_devices()
        for member in users:
            member.action = "refresh"
        if user.id == room.capitan_id:
            room.video_id = vid_id
        db.session.commit()
        return redirect(url_for('room', token=token))
    else:
        return redirect(url_for('viewroom'))

@app.route('/room/<string:token>/choose_video', methods=['GET', 'POST'])
def choose_video(token):
    user = anon_user()
    room = Room.query.filter_by(token=token).first()
    cap = room.capitan_id
    if room:
        return render_template('choose_video.html', user=cur_user(), items=Video.get(), cap=cap, room=room, anon=user)
    else:
        return redirect(url_for('viewroom'))

@app.route('/upload', methods=['GET', 'POST'])
@requiresauth
def upload():
    """
    Отвечает за вывод страницы загрузки и загрузку файлов
    :return: Страница загрузки
    """
    user = cur_user()
    
    form = UploadVideoForm(csrf_enabled=False)

    if form.validate_on_submit():
        if 'video' not in request.files:
            return redirect(request.url)
        file = request.files['video']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            video = save_video(file, form.title.data)

            if not video:
                form.video.errors.append(ValidationError('Ошибка при загрузке видео'))
                return render_template('upload_video.html', form=form, user=cur_user(),
                                       formats=app.config['ALLOWED_EXTENSIONS'])

            data = JSONDecoder().decode(form.geotag_data.data)
            if data['needed']:
                for coords in data['coords']:
                    gt = Geotag(*coords)
                    gt.save(video)

            if form.tags.data:
                tags = form.tags.data.split(',')
                for tag in tags:
                    tag_data = Tag(tag, video.id, user.id)
                    tag_data.save()
            return redirect(url_for("main"))
        elif not allowed_file(file.filename):
            form.video.errors.append(ValidationError('Некорректное разрешение'))

    if not form.geotag_data.data:
        form.geotag_data.data = dumps({'needed': False, 'coords': []})

    return render_template('upload_video.html', form=form, user=cur_user(), formats=app.config['ALLOWED_EXTENSIONS'])


@app.route('/result/', methods=['GET', 'POST'])
def result():
    user = cur_user()
    return render_template('rezult.html', pid='1', top=user.top, left=user.left, width=user.res_k)


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


@app.route('/cabinet/<string:usr>', methods=['GET', 'POST'])
@requiresauth
def cabinet(usr):
    """
    Отвечает за вывод страницы личного кабинета
    :return: Страница личного кабинета
    """

    video_list = Video.get()
    items = []
    user = cur_user()
    cabinet_owner = User.get(login=usr)

    if user == cabinet_owner:
        is_cabinet_settings_available = True
    else:
        is_cabinet_settings_available = False

    try:
        for item in video_list:
            if item.user_id == cabinet_owner.id:
                items.append(item)
    except:
        return render_template('404.html'), 404

    form = UserProfileForm()
    if form.validate_on_submit():
        user = cur_user()
        if form.change_name.data:
            user.change_name(form.change_name.data)
        if form.change_password.data:
            user.save(form.change_password.data)
        if form.channel_info.data:
            user.change_channel_info(form.channel_info.data)
        return redirect(url_for("cabinet", usr=cabinet_owner.login))
    return render_template('cabinet.html', form=form, user=cur_user(), items=items,
                           settings=is_cabinet_settings_available, usr=cabinet_owner)


@app.route('/play/<string:vid>', methods=['GET', 'POST'])
def play(vid):
    video = Video.get(video_id=vid)
    if not video:
        abort = Aborter() 
        return abort(404)
    
    user = cur_user()
    usr = User.get(login=video.user_login)

    if user and user not in video.viewers:
        video.add_viewer(user)

    likened = 0
    if user in video.likes:
        likened = 1
    if user in video.dislikes:
        likened = -1
    return render_template('play.html', user=user, vid=vid, video=video,lkd=likened,usr=usr)


@app.route('/video/map', methods=["GET"])
def videos_map():
    videos_with_coords = []
    user = cur_user()

    for video in Video.get():
        if video.geotags:
            videos_with_coords.append(video)

    return render_template('videos_map.html', user=user, videos=videos_with_coords)


@app.route('/views_story', methods=['GET', 'POST'])
def views_story():
    videos = Video.get()
    items = []
    for video in videos:
        if cur_user() in video.viewers:
            items.append(video)

    return render_template('views_story.html', user=cur_user(), items=items)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
