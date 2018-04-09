import unittest
import os
from flask import request
from web import app, db
from web.models import User, Video
from web.video_handler import save_video

TEST_DB = 'test.sqlite'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class TestModelUser(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.user = User('TestUser')
        self.user.save('testpassword')
        self.video = Video('TestVideo')
        self.video.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_has_need_fields(self):  # TODO Добавить проверки для остальных полей
        self.assertTrue(hasattr(self.user, "id"))
        self.assertTrue(hasattr(self.user, "login"))
        self.assertTrue(hasattr(self.user, "password"))
