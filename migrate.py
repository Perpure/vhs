from web import db
from web.models import *

db.drop_all()
db.create_all()
