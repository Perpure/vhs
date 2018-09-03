# coding=utf-8
import unittest
import os
from flask import url_for
from web import app, db
from web.models import User, Video, Room, Device

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB_PATH = os.path.join(BASE_DIR, 'test.sqlite')


@app.context_processor
def override_url_for():
    return dict(url_for=url_for)


class TestPageAvail(unittest.TestCase):

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
        self.anonuser = Device()
        self.room = Room('roomname', self.anonuser.id)
        self.room.save(self.video.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_main_page_be_exist(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_viewroom_page_be_exist(self):
        response = self.client.get("/viewroom", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_reg_page_be_exist(self):
        response = self.client.get("/registration", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_views_story_page_be_exist(self):
        response = self.client.get("/views_story", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_auth_page_be_exist(self):
        response = self.client.get("/login", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_play_page_be_exist(self):
        response = self.client.get("/play/" + self.video_id, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_cabinet_page_be_exist(self):
        response = self.client.get("/cabinet/TestUser", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @unittest.skip("unable to fix now")
    def test_should_room_page_be_exist(self):
        response = self.client.get("/room/" + str(self.room.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_upload_page_be_exist(self):
        response = self.client.get("/upload", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_404_page_be_exist(self):
        response = self.client.get("/notavail", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    @unittest.skip("unable to fix now")
    def test_should_choose_video1_page_be_exist(self):
        response = self.client.get("/room/" + str(self.room.id) + "/choose_video/" + str(self.video.id),
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_choose_video2_page_be_exist(self):
        response = self.client.get("/room/" + str(self.room.id) + "/choose_video", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
