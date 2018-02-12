from flask import redirect, render_template
from web import app


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')
