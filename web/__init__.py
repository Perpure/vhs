from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path="/static")
app.config.from_object("config")
db = SQLAlchemy(app)
Bootstrap(app)

import web.views

