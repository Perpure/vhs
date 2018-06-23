# coding=utf-8
"""Файл миграции приложения"""
from web import db
from web.models import *

db.drop_all()
db.create_all()
user = User("TestUser")
user.save("testpassword")
yellow = Color(color='#ffff00')
db.session.add(yellow)  # 1
cyan = Color(color='#00ffff')
db.session.add(cyan)  # 2
pink = Color(color='#ff00ff')
db.session.add(pink)  # 3
red = Color(color='#ff0000')
db.session.add(red)  # 4
blue = Color(color='#0000ff')
db.session.add(blue)  # 5
green = Color(color='#00ff00')
db.session.add(green)  # 6
user = User("tsarkov")
user.save("tsarkov1")
user = User("konnov")
user.save("konnov12")
user = User("mezentsev")
user.save("mezentsev")
user = User("vorobev")
user.save("vorobev1")
user = User("alekseev")
user.save("alekseev")
user = User("semenov")
user.save("semenov1")
user = User("shihanov")
user.save("shihanov")
user = User("dyachek")
user.save("dyachek1")
user = User("kucherov")
user.save("kucherov")
user = User("karimov")
user.save("karimov1")
user = User("valegov")
user.save("valegov1")
user = User("syomochkin")
user.save("syomochkin")
db.session.commit()
