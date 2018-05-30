# coding=utf-8
"""Файл запуска приложения"""


from imageio import plugins
from web import app

plugins.ffmpeg.download()
app.run(debug=True, host='0.0.0.0')
