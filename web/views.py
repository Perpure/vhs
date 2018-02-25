from flask import redirect, render_template, session, url_for
from web import app
from web.forms import RegForm, LogForm
from web.models import User


def cur_user():
    if 'Login' in session:
        return User.query.get(session['Login'])
    else:
        return None


def is_auth():
    return 'Login' in session



@app.route('/', methods=['GET', 'POST'])
def main():

    return render_template('main.html', user=cur_user())


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    user = None

    if form.validate_on_submit():
        user = User(form.login_reg.data)
        user.save(form.password_reg.data)
        session["Login"] = user.login
        return redirect(url_for("main"))

    return render_template('reg.html', form=form, user=user)


@app.route('/auth', methods=['GET', 'POST'])
def log():
    form = LogForm()
    user = None

    if form.submit_log.data and form.validate_on_submit():
        user = User.get(form.login_log.data)
        session["Login"] = user.login
        return redirect(url_for("main"))

    return render_template('auth.html', form=form, user=user)


@app.route('/cabinet', methods=['GET', 'POST'])
def cabinet():
    return render_template('Cabinet.html', user=is_auth())


@app.route("/logout", methods=['GET']) # FIXME FIXME FIXME FIXME FIXME FIXME
def logout():
    return render_template('main.html', user=cur_user())