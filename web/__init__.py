# coding=utf-8
"""Файл инициализации Flask-приложения"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads


app = Flask(__name__, static_url_path="/static")
app.config.from_object("config")
db = SQLAlchemy(app)
avatars = UploadSet('avatars', IMAGES)
configure_uploads(app, avatars)

import web.views
import web.service
