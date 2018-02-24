from web import db
from config import VIDEO_SAVE_PATH
import uuid




class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    path = db.Column(db.Column(db.Text(), unique=True, nullable=False))

    def pathgen(self, title):
        new_path = VIDEO_SAVE_PATH + title + uuid.uuid1()
        return (new_path)

    def save(self):
        pathgen(Video.title)
        db.session.commit()

    @staticmethod
    def get (self):
        Video.query.get(all)




