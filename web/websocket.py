# coding=utf-8
"""Файл взаимодействия WebSocket"""
from flask import jsonify, session
from flask_socketio import emit, send, join_room, leave_room
from web import app, socketio
from .models import AnonUser, Room


@socketio.on('join')
def on_join(room):
    print('joined')
    if 'anon_id' in session:
        print('anon is anon')
    join_room(room)


@socketio.on('leave')
def on_leave(room):
    leave_room(room)


@socketio.on('calibration_event')
def send_room_message(message):
    print('calibrate_ev')
    if message['data'] == 'calibrate':
        print('calibrate')
        user = AnonUser.query.get(session['anon_id'])
        color = user.color
        print(user.id)
        print(user.color)
        socketio.emit('my_response',
                      {'data': 'calibrate'},
                      broadccast=True)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
