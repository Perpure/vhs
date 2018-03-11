from flask import Flask
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])


app = Flask(__name__, static_url_path="/static")
app.config.from_object("config")
db = SQLAlchemy(app)

import web.views
