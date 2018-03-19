# coding=utf-8
"""Файл инициализации Flask-приложения"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/static")
app.config.from_object("config")
db = SQLAlchemy(app)

import web.views
