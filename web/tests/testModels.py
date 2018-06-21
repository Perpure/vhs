# coding=utf-8
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

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.user, "id"))
        self.assertTrue(hasattr(self.user, "login"))
        self.assertTrue(hasattr(self.user, "password"))

    def test_video_class_should_need_fields(self):
        self.assertTrue(hasattr(self.video, "id"))
        self.assertTrue(hasattr(self.video, "title"))
        self.assertTrue(hasattr(self.video, "path"))
        self.assertTrue(hasattr(self.video, "date"))
        self.assertTrue(hasattr(self.video, "user_id"))
        self.assertTrue(hasattr(self.video, "user_login"))
        self.assertTrue(hasattr(self.video, "geotags"))
        self.assertTrue(hasattr(self.video, "comments"))
        self.assertTrue(hasattr(self.video, "viewers"))

    def test_video_id_should_be_string(self):
        self.assertIsInstance(self.video.id, str)

    def test_video_title_should_be_string(self):
        self.assertIsInstance(self.video.title, str)

    def test_video_path_should_be_string(self):
        self.assertIsInstance(self.video.path, str)

    def test_video_user_id_should_be_string(self):
        self.assertIsInstance(self.video.user_id, int)

    def test_is_check_pass_work(self):
        self.assertTrue(self.user.check_pass('testpassword'))
        self.assertFalse(self.user.check_pass('faketestpassword'))

    def test_is_change_name_work(self):
        old = self.user.name
        self.user.change_name('newname')
        self.assertEqual('newname', self.user.name)
        self.assertNotEqual(old, self.user.name)

    def test_is_change_channel_info_work(self):
        old = self.user.channel_info
        self.user.change_channel_info('newinfo')
        self.assertEqual('newinfo', self.user.channel_info)
        self.assertNotEqual(old, self.user.channel_info)

    def test_is_get_method_work(self):
        self.assertEqual(User.get(self.user.id), self.user)


class TestModelVideo(unittest.TestCase):
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

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.video, "id"))
        self.assertTrue(hasattr(self.video, "title"))
        self.assertTrue(hasattr(self.video, "path"))
        self.assertTrue(hasattr(self.video, "date"))
        self.assertTrue(hasattr(self.video, "user_id"))
        self.assertTrue(hasattr(self.video, "user_login"))
        self.assertTrue(hasattr(self.video, "longitude"))
        self.assertTrue(hasattr(self.video, "latitude"))
        self.assertTrue(hasattr(self.video, "likes"))
        self.assertTrue(hasattr(self.video, "dislikes"))
        self.assertTrue(hasattr(self.video, "comments"))
        self.assertTrue(hasattr(self.video, "tags"))
        self.assertTrue(hasattr(self.video, "viewers"))
        self.assertTrue(hasattr(self.video, "geotags"))

    def test_is_add_viewer_method_works(self):
        old = len(self.video.viewers)
        self.video.add_viewer(self.user)
        self.assertEqual(old + 1, len(self.video.viewers))

    def test_is_add_like_method_works(self):
        old = len(self.video.likes)
        self.video.add_like(self.user)
        self.assertEqual(old + 1, len(self.video.likes))

    def test_is_add_dislike_method_works(self):
        old = len(self.video.dislikes)
        self.video.add_dislike(self.user)
        self.assertEqual(old + 1, len(self.video.dislikes))

    def test_is_delete_video_method_works(self):
        id = self.video.id
        with self.assertRaises(FileNotFoundError):
            self.video.delete_video()
