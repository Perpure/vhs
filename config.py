# coding=utf-8
"""Файл начальной инициализации приложения"""
import os
from imageio import plugins

# CSRF_ENABLED = True
SECRET_KEY = 'SuperSecretPassword'

basedir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'uploads')
VIDEO_SAVE_PATH = os.path.join(basedir, 'video')
ALLOWED_EXTENSIONS = {'mp4', 'ogv', 'mpeg', 'avi', 'mov', 'webm', 'flv'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
plugins.ffmpeg.download()
