# coding=utf-8
"""Файл начальной инициализации приложения"""
import os
from imageio import plugins

# CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']

basedir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'uploads')
VIDEO_SAVE_PATH = os.path.join(basedir, 'uploads/videos')
ALLOWED_EXTENSIONS = {'mp4', 'ogv', 'mpeg', 'avi', 'mov', 'webm', 'flv'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MB = 1 << 20
BUFF_SIZE = 10 * MB
plugins.ffmpeg.download()
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
CAPTCHA_PUBLIC_KEY = os.environ['CAPTCHA_PUBLIC_KEY']
CAPTCHA_PRIVATE_KEY = os.environ['CAPTCHA_PRIVATE_KEY']
