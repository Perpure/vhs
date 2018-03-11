# coding=utf-8
"""Контроллер"""
import hashlib
from flask import redirect, render_template, session, url_for,\
    make_response, request
from werkzeug.utils import secure_filename
from web import app
from web.forms import RegForm, LogForm, UploadVideoForm
from web.models import User, Video
from .helper import read_image, requiresauth, cur_user, allowed_file


@app.route('/images/<int:pid>.jpg')
def get_image(pid):
    """

    :param pid:
    :return:
    """
    image_binary = read_image(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response


@app.route('/', methods=['GET', 'POST'])
def main():
    """
    Отвечает за вывод шаблона главной страницы
    :return: Шаблон главной страницы
    """
    return render_template('main.html', user=cur_user())


@app.route('/calibrate', methods=['GET', 'POST'])
def multicheck():
    """
    Отвечает за вывод страницы калибровки
    :return: Страница калибровки
    """
    return render_template('color.html', color="#FF0000")


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
            ext = secure_filename(file.filename).split('.')[-1]
            video_hash = hashlib.md5(file.read()).hexdigest()
            file.seek(0)

            video = Video(form.title.data)
            file.save(video.save(video_hash, ext))

            return redirect(request.url)

    return render_template('upload_video.html', form=form, user=cur_user())


@app.route('/rezult1', methods=['GET', 'POST'])
def rezult1():
    """
    Выводит rezult.html с заданными параметрами
    :return: Выводит rezult.html
    """
    return render_template('rezult.html',
                           pid=1, top=0, left=0, right=0, bottom=0)


@app.route('/rezult2', methods=['GET', 'POST'])
def rezult2():
    """
    Выводит rezult.html с заданными параметрами
    :return: Выводит rezult.html
    """
    return render_template('rezult.html',
                           pid=1, top=0, left=-400, right=0, bottom=0)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    """
    Отвечает за вывод страницы регистрации и регистрацию
    :return: Страница регистрации
    """
    form = RegForm()
    user = None

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
    user = None

    if form.submit_log.data and form.validate_on_submit():
        user = User.get(form.login_log.data)
        session["Login"] = user.login
        return redirect(url_for("main"))

    return render_template('auth.html', form=form, user=cur_user())


@app.route('/cabinet', methods=['GET', 'POST'])
@requiresauth
def cabinet():
    """
    Отвечает за вывод страницы личного кабинета
    :return: Страница личного кабинета
    """
    return render_template('cabinet.html', user=cur_user())


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Отвечает за выход пользователя
    :return: Редирект /
    """
    if 'Login' in session:
        session.pop('Login')
    return redirect('/')


@app.route('/play', methods=['GET', 'POST'])
def play():
    """
    Отвечает за вывод страницы плеера и комментариев
    :return: Страница проигрывания видео
    """
    return render_template('play.html', user=cur_user())


@app.errorhandler(403)
def forbidden(e):
    """
    Обрабатывает ошибку 403
    :param e:
    :return: Страница ошибки 403
    """
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    """
    Обрабатывает ошибку 404
    :param e:
    :return: Страница ошибки 404
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    Обрабатывает ошибку 500
    :param e:
    :return: Страница ошибки 500
    """
    return render_template('500.html'), 500
