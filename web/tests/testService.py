# coding=utf-8
import unittest
import os
from web import app, db
from web.models import User, Video, Room, AnonUser, Comment

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB_PATH = os.path.join(BASE_DIR, 'test.sqlite')


class TestService(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB_PATH
        self.client = app.test_client()
        db.create_all()
        self.user = User('TestUser')
        self.user.save('testpassword')
        self.video = Video('TestVideo')
        self.video.save(hash='Teststring', user=self.user)
        self.video_id = self.video.id
        self.comment = Comment('Text', self.video.id, self.user.id)
        self.comment.save()
        self.anonuser = AnonUser()
        self.anonuser2 = AnonUser()
        self.room = Room('roomname', self.anonuser.id)
        self.room.save(self.video.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_logout_page_be_exist(self):
        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_is_askAct_work(self):
        response = self.client.get("/askAct/" + str(self.room.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_is_askNewComm_work(self):
        response = self.client.get("/askNewComm/" + str(self.video.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_is_getNewComm_work(self):
        response = self.client.get("/getNewComm/" + str(self.video.id) + '/' + str(self.comment.id),
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_is_likeVideo_work(self):
        response = self.client.get("/likeVideo/" + str(self.video.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_is_dislikeVideo_work(self):
        response = self.client.get("/dislikeVideo/" + str(self.video.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
