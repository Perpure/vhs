from web import db
from web.models import *

db.drop_all()
db.create_all()

user = User("TestUser")
user.save("testpassword")
r=Room(token='asdasds')
db.session.commit()
