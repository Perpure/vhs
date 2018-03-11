from flask import redirect, render_template, session, url_for,\
    make_response, request
from web import app
from web.forms import RegForm, LogForm, UploadVideoForm
from web.models import User, Video
from web import ALLOWED_EXTENSIONS
from .helper import read_image, requiresauth, cur_user
from werkzeug.utils import secure_filename
import hashlib


@app.route('/images/<int:pid>.jpg')
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


def allowed_file(filename):
    return ('.' in filename and
            filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS)


@app.route('/calibrate', methods=['GET', 'POST'])
def multicheck():
    return render_template('color.html', color="#FF0000")


@app.route('/upload', methods=['GET', 'POST'])
@requiresauth
def upload():
    form = UploadVideoForm(csrf_enabled=False)
    if form.validate_on_submit():
        if 'video' not in request.files:
            return redirect(request.url)

        file = request.files['video']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            ext = secure_filename(file.filename).split('.')[-1]
            hash = hashlib.md5(file.read()).hexdigest()
            file.seek(0)

            video = Video(form.title.data)
            file.save(video.save(hash, ext))

            return redirect(request.url)

    return render_template('upload_video.html', form=form, user=cur_user())


@app.route('/rezult1', methods=['GET', 'POST'])
def rezult1():
    return render_template('rezult.html',
                           pid=1, top=0, left=0, right=0, bottom=0)


@app.route('/rezult2', methods=['GET', 'POST'])
def rezult2():
    return render_template('rezult.html',
                           pid=1, top=0, left=-400, right=0, bottom=0)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
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
    return render_template('Cabinet.html', user=cur_user())


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'Login' in session:
        session.pop('Login')
    return redirect('/')


@app.route('/play', methods=['GET', 'POST'])
def play():
    return render_template('play.html', user=cur_user())


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
