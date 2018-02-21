from web import db





class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    path = db.Column(db.Column(db.Text(), unique=True, nullable=False))

    def save(self):
        db.session.commit()

    def get (self):
        return chr(self.id)


def pathgen(name):
    new_path = 'src/video/' + name
    return (new_path)


