# coding=utf-8
"""Файл инициализации Flask-приложения"""
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads


app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app)
app.config.from_object("config")
db = SQLAlchemy(app)
avatars = UploadSet('avatars', IMAGES)
backgrounds = UploadSet('backgrounds', IMAGES)
calibrate = UploadSet('calibrate', IMAGES)
configure_uploads(app, (avatars, backgrounds, calibrate))


import web.views
import web.service
import web.websocket
