import unittest
import os
from web import app, db
from web.models import User

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
        self.user = User('Testuser')
        self.user.save('testpassword')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_has_need_fields(self):  # TODO Добавить проверки для остальных полей
        self.assertTrue(hasattr(self.user, "id"))
        self.assertTrue(hasattr(self.user, "login"))
        self.assertTrue(hasattr(self.user, "password"))
