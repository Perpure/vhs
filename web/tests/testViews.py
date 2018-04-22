import unittest
import os
from web import app, db
from web.models import User, Video

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB_PATH = os.path.join(BASE_DIR, 'test.sqlite')


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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_main_page_be_exist(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_viewroom_page_be_exist(self):
        response = self.client.get("/viewroom", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_addroom_page_be_exist(self):
        response = self.client.get("/addroom", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_should_reg_page_be_exist(self):
        response = self.client.get("/reg", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_auth_page_be_exist(self):
        response = self.client.get("/auth", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_play_page_be_exist(self):
        response = self.client.get("/play/" + self.video_id, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_should_cabinet_page_be_exist(self):
        response = self.client.get("/cabinet", follow_redirects=True)
        self.assertEqual(response.status_code, 403)

    def test_should_upload_page_be_exist(self):
        response = self.client.get("/upload", follow_redirects=True)
        self.assertEqual(response.status_code, 403)

    def test_should_404_page_be_exist(self):
        response = self.client.get("/notavail", follow_redirects=True)
        self.assertEqual(response.status_code, 404)
