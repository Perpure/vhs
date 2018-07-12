# coding=utf-8
import unittest
import os
from web import app, db
from web.models import User, Video
from flask import session

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB = 'test.sqlite'


class TestHelper(unittest.TestCase):
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
