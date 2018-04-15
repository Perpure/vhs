# coding=utf-8
"""Файл миграции приложения"""
from web import db
from web.models import *

db.drop_all()
db.create_all()
user = User("TestUser")
user.save("testpassword")
red = Color(color='#ff0000')
db.session.add(red)   #1
blue = Color(color='#0000ff')
db.session.add(blue)  #2
green = Color(color='#00ff00')
db.session.add(green) #3
brown = Color(color='#996633')
db.session.add(brown) #4
white = Color(color='#ffffff')
db.session.add(white) #5
pink = Color(color='#ff33cc')
db.session.add(pink)  #6
user = User("11111")
user.save("11111111")
db.session.commit()
user = User("22222")
user.save("22222222")



