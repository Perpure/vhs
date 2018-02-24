from flask import redirect, render_template, session, url_for
from web import app
from web.forms import RegForm, LogForm
from web.models import User


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


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


# @app.route("/logout", methods=['GET'])
# def logout():
#     session.pop("VotesLogin", None)
#     return redirect(url_for("main"))