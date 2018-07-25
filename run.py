# coding=utf-8
"""Файл запуска приложения"""


from web import app, socketio
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.FATAL)
app.run(debug=True, host='0.0.0.0', threaded=True)
socketio.run(app, debug=True)
app.logger.disabled = True

