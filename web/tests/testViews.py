import unittest
import os
from web import app, db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB_PATH = os.path.join(BASE_DIR, 'test.sqlite')


class TestMainPage(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB_PATH
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_main_page_be_exist(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
