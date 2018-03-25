# coding=utf-8
"""Файл запуска приложения"""
import imageio

imageio.plugins.ffmpeg.download()

from web import app

app.run(debug=True)
