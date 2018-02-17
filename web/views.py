from flask import redirect, render_template
from web import app


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/calibrate', methods=['GET', 'POST'])
def multicheck():
    return render_template('color.html', color="#FF0000")

@app.route('/rezult', methods=['GET', 'POST'])
def rezult():
    return render_template('rezult.html')
