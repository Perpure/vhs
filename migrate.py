# coding=utf-8
"""Файл миграции приложения"""
from web import db
from web.models import *

db.drop_all()
db.create_all()
user = User("TestUser")
user.save("testpassword")
yellow = Color(color='#ffff00')
db.session.add(yellow)#1
cyan = Color(color='#00ffff')
db.session.add(cyan)  #2
pink = Color(color='#ff00ff')
db.session.add(pink)  #3
red = Color(color='#ff0000')
db.session.add(red)   #4
blue = Color(color='#0000ff')
db.session.add(blue)  #5
green = Color(color='#00ff00')
db.session.add(green) #6
user = User("11111")
user.save("11111111")
db.session.commit()
user = User("22222")
user.save("22222222")
user = User("33333")
user.save("33333333")
user = User("44444")
user.save("44444444")
user = User("55555")
user.save("55555555")
user = User("66666")
user.save("66666666")
user = User("77777")
user.save("77777777")
db.session.commit()



