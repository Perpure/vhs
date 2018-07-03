# coding=utf-8
"""Файл взаимодействия WebSocket"""
from flask import jsonify, session
from flask_socketio import emit, send, join_room, leave_room
from web import app, socketio
from .models import AnonUser, Room


@socketio.on('join')
def on_join(room):
    join_room(room)


@socketio.on('leave')
def on_leave(room):
    leave_room(room)


@socketio.on('multiscreen_set_calibrate')
def multiscreen_show_calibrate(message):
    socketio.emit('multiscreen_show_calibrate',
                  broadcast=True)
