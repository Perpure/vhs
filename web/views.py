from flask import redirect, render_template
from web import app


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


@app.route('/video', methods=['GET', 'POST'])
def video():
    return render_template('video.html')
