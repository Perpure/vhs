import os
from flask import Flask
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = '/videos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

app = Flask(__name__)
app.config.from_object("config")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
import web.views


