# coding=utf-8
"""Файл начальной инициализации приложения"""
import os

# CSRF_ENABLED = True
SECRET_KEY = 'SuperSecretPassword'

basedir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
VIDEO_SAVE_PATH = os.path.join(basedir, 'video')
