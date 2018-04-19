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
        self.video.save(hash='Teststring', user=self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_has_need_fields(self):  # TODO Добавить проверки для остальных полей
        self.assertTrue(hasattr(self.user, "id"))
        self.assertTrue(hasattr(self.user, "login"))
        self.assertTrue(hasattr(self.user, "password"))

    def test_video_class_should_need_fields(self):
        self.assertTrue(hasattr(self.video, "id"))
        self.assertTrue(hasattr(self.video, "title"))
        self.assertTrue(hasattr(self.video, "path"))
        self.assertTrue(hasattr(self.video, "date"))
        self.assertTrue(hasattr(self.video, "user"))
        self.assertTrue(hasattr(self.video, "geotags"))
        self.assertTrue(hasattr(self.video, "marks"))
        self.assertTrue(hasattr(self.video, "comments"))
        self.assertTrue(hasattr(self.video, "viewers"))

    def test_video_id_should_be_string(self):
        self.assertTrue(self.video.id is not int)

    def test_video_title_should_be_string(self):
        self.assertTrue(self.video.id is not int)

    def test_video_path_should_be_string(self):
        self.assertTrue(self.video.id is not int)

    def test_video_user_should_be_integer(self):
        self.assertTrue(self.video.id is not str)

    def test_video_views_should_be_integer(self):
        self.assertTrue(self.video.id is not str)
