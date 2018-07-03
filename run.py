# coding=utf-8
"""Файл запуска приложения"""


from web import app, socketio


app.run(debug=True, host='0.0.0.0', threaded=True)
socketio.run(app, debug=True)
