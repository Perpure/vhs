import unittest
from web import app
from wtforms import IntegerField, StringField, SubmitField
from web.forms import LogForm


class TestLogForm(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context():
            self.form = LogForm()

    def tearDown(self):
        del self.form

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.form, "login_log"))
        self.assertTrue(hasattr(self.form, "password_log"))
        self.assertTrue(hasattr(self.form, "submit_log"))
        self.assertTrue(hasattr(self.form, "submit_main"))

    def test_should_login_log_field_is_string_field(self):
        self.assertIsInstance(self.form.login_log, StringField)

    def test_should_password_log_field_is_string_field(self):
        self.assertIsInstance(self.form.password_log, StringField)

    def test_should_submit_log_field_is_submit_field(self):
        self.assertIsInstance(self.form.submit_log, SubmitField)

    def test_should_submit_main_field_is_submit_field(self):
        self.assertIsInstance(self.form.submit_main, SubmitField)
