from web import db
from web.models import Video

db.drop_all()
db.create_all()
