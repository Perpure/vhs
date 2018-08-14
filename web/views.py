# coding=utf-8
import os
import json
from wtforms.validators import ValidationError
from flask import redirect, render_template, session, url_for, request
from flask.json import JSONDecoder, dumps
from werkzeug.exceptions import Aborter
from config import basedir, CAPTCHA_PUBLIC_KEY
from web import app, db, avatars, backgrounds, socketio
from web.forms import RegForm, LogForm, UploadVideoForm, JoinForm, RoomForm, UploadImageForm, \
    UserProfileForm, AddRoomForm, AccountSettingsForm, FeedbackForm
from web.models import User, Video, Room, Color, Geotag, Tag, Device, RoomDeviceColorConnector, Feedback
from web.helper import cur_user, requiresauth, anon_user, image_loaded
from web.video_handler import save_video
from datetime import datetime
from flask_socketio import emit


@app.route('/', methods=['GET', 'POST'])
def main():
    user = cur_user()
    sub_items = []
    if user:
        subs = user.subscriptions
        for sub in subs:
            for video in sub.videos:
                sub_items.append(video)

    now = time = datetime.now(tz=None)
    video_pack = Video.get(need_geo=True)
    return render_template('main.html', user=user, items=video_pack[0], sub_items=sub_items,
                           now=now, geo_items=json.dumps([video.serialize() for video in video_pack[1]]))


@app.route('/createroom', methods=['GET', 'POST'])
def createroom():
    user = anon_user()
    user.action = ""
    db.session.commit()

    add_room_form = AddRoomForm(prefix="Submit_Add")

    if add_room_form.validate_on_submit():
        name = add_room_form.token.data
        room = Room(name=name, capitan_id=user.id)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('room', room_id=room.id))
    return render_template('create_room.html', user=cur_user(), add_room_form=add_room_form)


@app.route('/viewroom', methods=['GET', 'POST'])
def viewroom():
    user = anon_user()
    join_form = JoinForm(prefix="Submit_Join")
    user.action = ""
    db.session.commit()

    if join_form.validate_on_submit():
        room = Room.query.filter_by(name=str(join_form.token.data)).first()
        if room:
            return redirect(url_for('room', room_id=room.id))

    return render_template('viewroom.html', user=cur_user(), join_form=join_form,
                           rooms=Room.get()[::-1], anon=user)


@app.route('/room/<int:room_id>', methods=['GET', 'POST'])
def room(room_id):
    user = anon_user()
    room_form = RoomForm()
    room = Room.query.get(room_id)
    if room:
        room_map_url = str(room_id) + '_map'
        raw_user_rooms = RoomDeviceColorConnector.query.filter_by(anon=user)
        user_rooms = [rac.room for rac in raw_user_rooms]
        users = room.get_devices()

        if not (room in user_rooms) and (room.captain != user):
            color_id = len(users) + 1
            if color_id > 6:
                return redirect(url_for('viewroom'))
            col = Color.query.get(color_id)
            rac = RoomDeviceColorConnector(anon=user, room=room, color=col)
            db.session.add(rac)
            socketio.emit('update', len(users) + 2, broadcast=True)

        users = room.get_devices()

        for member in users:
            rac = RoomDeviceColorConnector.query.filter_by(room=room,
                                                           anon=member).first()
            member.color = rac.color.color
            db.session.commit()

        image_form = UploadImageForm()
        if image_form.validate_on_submit():
            return image_loaded(request, room, user, users, image_form, room_form)

        return render_template('room.html', room=room, user=cur_user(), users=users,
                               count=len(users) + 1,
                               image_form=image_form, room_form=room_form, loaded=False, anon=user,
                               room_map=room_map_url,
                               map_ex=os.path.exists(basedir + '/images/' + str(room.id) + '_map.jpg'))
    else:
        return redirect(url_for('viewroom'))


@app.route('/room/<int:room_id>/choose_video/<string:vid_id>', methods=['GET', 'POST'])
def choosed_video(room_id, vid_id):
    user = anon_user()
    room = Room.query.get(room_id)
    vid = Video.query.get(vid_id)
    if vid and room:
        if user.id == room.capitan_id:
            room.video_id = vid_id
        db.session.commit()
        return redirect(url_for('room', room_id=room_id))
    else:
        return redirect(url_for('viewroom'))


@app.route('/room/<int:room_id>/choose_video', methods=['GET', 'POST'])
def choose_video(room_id):
    user = anon_user()
    room = Room.query.get(room_id)
    cap = room.capitan_id
    if room:
        now = time = datetime.now(tz=None)
        sub_items = []
        real_user = cur_user()
        if real_user:
            subs = real_user.subscriptions
            for sub in subs:
                for video in sub.videos:
                    sub_items.append(video)
        video_pack = Video.get(need_geo=True)
        return render_template('choose_video.html', user=cur_user(), items=video_pack[0],
                               cap=cap, room=room, anon=user, now=now, sub_items=sub_items,
                               geo_items=json.dumps([video.serialize() for video in video_pack[1]]))
    else:
        return redirect(url_for('viewroom'))


@app.route('/room/<int:room_id>/choose_youtube')
def choose_youtube_video(room_id):
    return render_template('choose_youtube.html')


@app.route('/upload', methods=['GET', 'POST'])
@requiresauth
def upload():
    """
    Отвечает за вывод страницы загрузки и загрузку файлов
    :return: Страница загрузки
    """

    form = UploadVideoForm()

    if form.validate_on_submit():
        file = request.files['video']

        video = save_video(file, form.title.data)

        if not video:
            form.video.errors.append(ValidationError('Ошибка при загрузке видео'))
            return render_template('upload_video.html', form=form, user=cur_user(),
                                   formats=app.config['ALLOWED_EXTENSIONS'])

        data = JSONDecoder().decode(form.geotag_data.data)
        if data['needed']:
            for coords in data['coords']:
                geo_tag = Geotag(*coords)
                video.geotags.append(geo_tag)

        if form.tags.data:
            tags = form.tags.data.split(',')
            for tag_name in tags:
                video_tag = Tag.create_unique(text=tag_name)
                video.tags.append(video_tag)
        db.session.commit()
        return redirect(url_for("main"))

    if not form.geotag_data.data:
        form.geotag_data.data = dumps({'needed': False, 'coords': []})

    return render_template('upload_video.html', form=form, user=cur_user(), formats=app.config['ALLOWED_EXTENSIONS'])


@app.route('/registration', methods=['GET', 'POST'])
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

    return render_template('user/registration.html', form=form, user=cur_user())


@app.route('/login', methods=['GET', 'POST'])
def log():
    """
    Отвечает за вывод страницы входа и вход
    :return: Страница входа
    """

    form = LogForm()

    if form.validate_on_submit():
        session["Login"] = form.login_log.data
        return redirect(url_for("main"))

    return render_template('user/login.html', form=form, user=cur_user())


@app.route('/cabinet/<string:usr>', methods=['GET', 'POST'])
@requiresauth
def cabinet(usr, tab=0):
    """
    Отвечает за вывод страницы личного кабинета
    :return: Страница личного кабинета
    """

    video_list = Video.get()
    user = cur_user()
    cabinet_owner = User.get(login=usr)
    is_cabinet_settings_available = False

    if user == cabinet_owner:
        is_cabinet_settings_available = True

    items = cabinet_owner.videos

    form = UserProfileForm()
    form_acc = AccountSettingsForm()
    if request.method == 'POST':
        form_name = request.form['form-name']
        tab = 2
        if form_name == 'form':
            tab = 1
        if form_name == 'form' and form.validate():
            tab = 1
            user = cur_user()
            folder = str(user.id)
            if form.change_name.data:
                user.change_name(form.change_name.data)
            if form.channel_info.data:
                user.change_channel_info(form.channel_info.data)
            if 'avatar' in request.files:
                avatar_url = avatars.save(form.avatar.data, folder=folder)
                user.update_avatar(json.dumps({"url": avatar_url}))
            if 'background' in request.files:
                background_url = backgrounds.save(form.background.data, folder=folder)
                user.update_background(json.dumps({"url": background_url}))
            return redirect(url_for("cabinet", usr=cabinet_owner.login, tab=tab))
        elif form_name == 'form_acc' and form_acc.validate():
            tab = 2
            user = cur_user()
            if form_acc.change_password.data:
                user.save(form_acc.change_password.data)
            return redirect(url_for("cabinet", usr=cabinet_owner.login, tab=tab))
    now = time = datetime.now(tz=None)
    return render_template('user/cabinet.html', form=form, form_acc=form_acc, user=user, items=items,
                           settings=is_cabinet_settings_available, usr=cabinet_owner,
                           subscribed=(user in cabinet_owner.subscribers), now=now, tab=tab)


@app.route('/play/<string:vid>', methods=['GET', 'POST'])
def play(vid):
    video = Video.get(video_id=vid)
    if not video:
        abort = Aborter()
        return abort(404)

    user = cur_user()
    usr = User.get(login=video.user.login)

    if user and user not in video.viewers:
        video.add_viewer(user)

    likened = 0
    if user in video.likes:
        likened = 1
    if user in video.dislikes:
        likened = -1
    return render_template('video_page.html', user=user, vid=vid, video=video, lkd=likened,
                           usr=usr, subscribed=(user in usr.subscribers))


@app.route('/video/map', methods=["GET"])
def videos_map():
    videos_with_coords = []
    user = cur_user()

    for video in Video.get():
        if video.geotags:
            videos_with_coords.append(video)

    return render_template('videos_map.html', user=user, videos=videos_with_coords)


@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    user = cur_user()

    form = FeedbackForm()
    if form.validate_on_submit():
        email = form.feedback_email.data
        form.feedback_email.data = ''
        text = form.feedback_text.data
        form.feedback_text.data = ''
        feedback = Feedback(email, text)

        return render_template('feedback.html', user=user, form=form, CAPTCHA_KEY=CAPTCHA_PUBLIC_KEY,
                               message='Спасибо за ваше сообщение!')

    return render_template('feedback.html', user=user, form=form, CAPTCHA_KEY=CAPTCHA_PUBLIC_KEY, message='')


@app.route('/views_story', methods=['GET', 'POST'])
def views_story():
    videos = Video.get()
    items = []
    for video in videos:
        if cur_user() in video.viewers:
            items.append(video)

    return render_template('views_story.html', user=cur_user(), items=items)


@app.route('/subscriptions', methods=['GET', 'POST'])
def subs_s():
    user = cur_user()
    subs = user.subscriptions
    return render_template('subs.html', user=user, subs=subs)


@app.route('/search')
def search_results():
    user = cur_user()
    now = time = datetime.now(tz=None)
    return render_template('search_results.html', user=user, now=now, presearch=0)


@app.route('/search/<string:presearch>')
def search_results_unvoid(presearch=None):
    user = cur_user()
    now = time = datetime.now(tz=None)
    return render_template('search_results.html', user=user, now=now, presearch=presearch)


@app.route('/fact')
def fact():
    user = cur_user()
    return render_template('fact.html', user=user)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', user=cur_user()), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=cur_user()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', user=cur_user()), 500
