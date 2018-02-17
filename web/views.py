from flask import redirect, render_template, session, url_for
from web import app


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


@app.route("/logout", methods=['GET'])
def logout():
    session.pop("VotesLogin", None)
    return redirect(url_for("main"))