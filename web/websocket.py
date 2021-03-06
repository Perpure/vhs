﻿# coding=utf-8
"""Файл взаимодействия WebSocket"""
from flask import jsonify, session
from flask_socketio import emit, send, join_room, leave_room
from web import app, socketio, db
from .models import Device, Room
from web.helper import cur_user


@socketio.on('join')
def on_join(room, id):
    if 'anon_id' in session:
        cur_room = Room.query.get(room)
        user = Device.query.get(session['anon_id'])
        user.socket_id = id
        db.session.commit()
    join_room(room)


@socketio.on('leave')
def on_leave(room):
    leave_room(room)


@socketio.on('multiscreen_set_calibrate')
def multiscreen_show_calibrate(msg):
    socketio.emit('multiscreen_show_calibrate', room=msg)


@socketio.on('multiscreen_set_show')
def multiscreen_show_result(message):
    room_id = message
    if 'anon_id' in session:
        room = Room.query.get(room_id)
        users = room.get_devices()
        for member in users:
            noSound = True
            if member == users[0]:
                noSound = False
            params = {'top': member.top, 'left': member.left, 'scale': member.scale, 'noSound': noSound}
            emit('multiscreen_show_result', params, room=member.socket_id)


@socketio.on('multiscreen_set_pause')
def multiscreen_show_pause(msg):
    socketio.emit('multiscreen_show_pause', room=msg)


@socketio.on('multiscreen_set_stop')
def multiscreen_show_stop(msg):
    socketio.emit('multiscreen_show_stop', room=msg)


@socketio.on('multiscreen_refresh')
def multiscreen_refresh(msg):
    socketio.emit('refresh', room=msg)


@socketio.on('ended')
def video_ended(msg):
    cur_room = Room.query.get(msg)
    captain = cur_room.captain
    socketio.emit('video_ended', room=captain.socket_id)
