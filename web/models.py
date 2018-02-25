from web import db
from config import VIDEO_SAVE_PATH
import uuid




class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    path = db.Column(db.Column(db.Text(),  nullable=False))

    def __init__(self, title,path):
        self.title = title
        self.path  = path

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id=None):
        if id == None: return Video.query.all()
        return Video.query.get(id)


