from web import app, db
from web.forms import RegForm, LogForm, UploadVideoForm, JoinForm, RoomForm, UploadImageForm, \
    UserProfileForm, AddRoomForm, AddCommentForm, SearchingVideoForm, LikeForm, DislikeForm
from web.models import User, Video, Room, Color, Comment, Geotag, Tag, AnonUser
from web.helper import read_image, read_video, allowed_image, allowed_file, cur_user, is_true_pixel, \
    read_multi, parse, requiresauth
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


@app.route('/', methods=['GET', 'POST'])
def main():
    form = SearchingVideoForm()
    if form.validate_on_submit():
        sort = ""

        if form.date.data:
            sort += "date"
        if form.views.data:
            sort += "views"
        if form.search.data:
            return render_template('main.html', form=form, user=cur_user(), items=Video.get(search=form.search.data,
                                                                                            sort=sort))

        return render_template('main.html', form=form, user=cur_user(), items=Video.get(sort=sort))

    return render_template('main.html', form=form, user=cur_user(), items=Video.get())


@app.route('/viewroom', methods=['GET', 'POST'])
def viewroom():
    if not('anon_id' in session):
        user = AnonUser()
        session['anon_id'] = user.id
    else:
        user = AnonUser.query.filter_by(id=session['anon_id']).first()
        if not(user):
            user = AnonUser()
            session['anon_id'] = user.id

    join_form = JoinForm(csrf_enabled=False, prefix="Submit_Join")
    user.action = ""
    db.session.commit()
    add_room_form = AddRoomForm(csrf_enabled=False, prefix="Submit_Add")
    if add_room_form.is_submitted() and add_room_form.validate_on_submit():
        token = add_room_form.token.data
        room = Room(token=token, capitan_id=user.id)
        for i in range(1, 7):
            room.Color.append(Color.query.filter_by(id=str(i)).first())
        db.session.add(room)
        db.session.commit()
        user.rooms.append(room)
        db.session.commit()
        return redirect(url_for('addroom', token=add_room_form.token.data))

    if join_form.is_submitted() and join_form.validate_on_submit():
        if Room.query.filter_by(token=str(join_form.token.data)):
            return redirect(url_for('room', token=join_form.token.data))
    rooms = user.rooms

    return render_template('viewroom.html', user=cur_user(), join_form=join_form,add_room_form=add_room_form,
                           rooms=Room.query.all(), anon = user)

@app.route('/addroom/<string:token>', methods=['GET', 'POST'])
def addroom(token):
    return render_template('addroom.html', user=cur_user(), token=token)


@app.route('/room/<string:token>', methods=['GET', 'POST'])
def room(token):
    if not('anon_id' in session):
        user = AnonUser()
        session['anon_id'] = user.id
    else:
        user = AnonUser.query.filter_by(id=session['anon_id']).first()
        if not(user):
            user = AnonUser()
            session['anon_id'] = user.id

    Room_Form = RoomForm()
    calibrate_url = None
    result_url = None
    color = None
    if user:
        room = Room.query.filter_by(token=token).first()
        room_map_url = token+'_map'
        if Room_Form.validate_on_submit():
            for i in range(len(room.color_user.split(';'))):
                ID = room.color_user.split(';')[i].split(',')[0]
                AnonUser.query.filter_by(id=ID).first().action = "calibrate"
            db.session.commit()

        if not ((room in user.rooms)):
            user.rooms.append(room)
            if room.color_user:
                color_id = len(room.color_user.split(';')) + 1
                room.color_user += ';' + str(user.id) + ',' + str(color_id)
            else:
                room.color_user = str(user.id) + ',1'
            db.session.commit()
        users = room.user
        for member in users[1:]:
            colors = room.color_user.split(';')
            for i in range(len(colors)):
                if colors[i].split(',')[0] == str(member.id):
                    color = Color.query.filter_by(id=colors[i].split(',')[1]).first().color
                    member.color = color
                    db.session.commit()
                    break
        image_form = UploadImageForm(csrf_enabled=False)
        if image_form.validate_on_submit():
            if 'image' not in request.files:
                return render_template('room.html', room=room, user=cur_user(),
                                       calibrate_url=calibrate_url, color=user.color, users=users,
                                       image_form=UploadImageForm(csrf_enabled=False),
                                       result_url=result_url, Room_Form=Room_Form, loaded=False,
                                       room_map=room_map_url, anon=user, count=len(users))

            file = request.files['image']
            if file.filename == '':
                return render_template('room.html', room=room, user=cur_user(),
                                       calibrate_url=calibrate_url, color=user.color, users=users,
                                       image_form=UploadImageForm(csrf_enabled=False),
                                       result_url=result_url, Room_Form=Room_Form, loaded=False,
                                       room_map=room_map_url, anon=user, count=len(users))

            if file and allowed_image(file.filename):
                file.save(basedir + '/images/' + room.token + '.' + file.filename.split('.')[-1].lower())
                try:
                    parse(room, users[1:], basedir + '/images/' + room.token + '.jpg')
                except:
                    return render_template('room.html', room=room, user=cur_user(),
                                               calibrate_url=calibrate_url, color=user.color, users=users,
                                               image_form=image_form, result_url=result_url, count=len(users),
                                               Room_Form=Room_Form, loaded=True, room_map=room_map_url, anon=user,
                                               msg="Мы не смогли идентифицировать устройства, попробуйте загрузить другую фотографию.")
                return render_template('room.html', room=room, user=cur_user(),
                                       calibrate_url=calibrate_url, color=user.color, users=users,
                                       image_form=image_form, result_url=result_url, anon=user,
                                       Room_Form=Room_Form, loaded=True, room_map=room_map_url, count=len(users))

    else:
        return redirect(url_for('log'))
    return render_template('room.html', room=room, user=cur_user(),
                           calibrate_url=calibrate_url, color=user.color, users=users, count=len(users),
                           image_form=image_form, result_url=result_url, Room_Form=Room_Form, loaded=False, anon=user,
                           room_map=room_map_url, map_ex=os.path.exists(basedir + '/images/' + room.token + '_map.jpg'))

@app.route('/room/<string:token>/choose_video/<string:vid_id>', methods=['GET', 'POST'])
def choosed_video(token,vid_id):
    if not('anon_id' in session):
        user = AnonUser()
        session['anon_id'] = user.id
    else:
        user = AnonUser.query.filter_by(id=session['anon_id']).first()
        if not(user):
            user = AnonUser()
            session['anon_id'] = user.id

    room = Room.query.filter_by(token=token).first()
    if user.id == room.capitan_id:
        room.video_id = vid_id
        db.session.commit()
    return redirect(url_for('room', token=token))

@app.route('/room/<string:token>/choose_video', methods=['GET', 'POST'])
def choose_video(token):
    if not('anon_id' in session):
        user = AnonUser()
        session['anon_id'] = user.id
    else:
        user = AnonUser.query.filter_by(id=session['anon_id']).first()
        if not(user):
            user = AnonUser()
            session['anon_id'] = user.id

    room = Room.query.filter_by(token=token).first()
    cap = room.capitan_id
    form = SearchingVideoForm()
    if form.validate_on_submit():
        sort = ""

        if form.date.data:
            sort += "date"
        if form.views.data:
            sort += "views"
        if form.search.data:
            return render_template('choose_video.html', form=form, user=cur_user(), items=Video.get(search=form.search.data,
                                                                                            sort=sort), cap=cap, room=room, anon=user)

        return render_template('choose_video.html', form=form, user=cur_user(), items=Video.get(sort=sort), cap=cap, room=room, anon=user)

    return render_template('choose_video.html', form=form, user=cur_user(), items=Video.get(), cap=cap, room=room, anon=user)


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
    form = AddCommentForm()
    like_form = LikeForm()
    dislike_form = DislikeForm()

    if user and user not in video.viewers:
        video.add_viewer(user)

    if like_form.like.data:
        video.add_like(user)
        if user in video.dislikes:
            video.dislikes.remove(user)
            db.session.add(user)
            db.session.commit()

    if dislike_form.dislike.data:
        video.add_dislike(user)
        if user in video.likes:
            video.likes.remove(user)
            db.session.add(user)
            db.session.commit()

    if form.validate_on_submit():
        comment = Comment(form.message.data, video.id, user.id)
        comment.save()

    likened = 0
    if user in video.likes:
        likened = 1
    if user in video.dislikes:
        likened = -1
    return render_template('play.html', user=user, vid=vid, video=video, form=form,
                           like_form=like_form, dislike_form=dislike_form,lkd=likened)


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
