import unittest
from web import app
from wtforms import IntegerField, StringField, SubmitField, ValidationError, PasswordField, FileField
from web.forms import LogForm, RegForm, UserProfileForm, AddCommentForm, AddRoomForm, JoinForm, \
    UploadVideoForm, BooleanField, HiddenField


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


class TestRegForm(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context():
            self.form = RegForm()

    def tearDown(self):
        del self.form

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.form, "login_reg"))
        self.assertTrue(hasattr(self.form, "password_reg"))
        self.assertTrue(hasattr(self.form, "confirm_reg"))
        self.assertTrue(hasattr(self.form, "submit_reg"))
        self.assertTrue(hasattr(self.form, "submit_main"))

    def test_should_login_reg_field_is_string_field(self):
        self.assertIsInstance(self.form.login_reg, StringField)

    def test_should_password_reg_field_is_password_field(self):
        self.assertIsInstance(self.form.password_reg, PasswordField)

    def test_should_confirm_reg_field_is_password_field(self):
        self.assertIsInstance(self.form.password_reg, PasswordField)

    def test_should_submit_reg_field_is_submit_field(self):
        self.assertIsInstance(self.form.submit_reg, SubmitField)

    def test_should_submit_main_field_is_submit_field(self):
        self.assertIsInstance(self.form.submit_main, SubmitField)


class TestUserProfileForm(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context():
            self.form = UserProfileForm()

    def tearDown(self):
        del self.form

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.form, "change_name"))
        self.assertTrue(hasattr(self.form, "change_password"))
        self.assertTrue(hasattr(self.form, "change_avatar"))
        self.assertTrue(hasattr(self.form, "change_background"))
        self.assertTrue(hasattr(self.form, "channel_info"))
        self.assertTrue(hasattr(self.form, "current_password"))
        self.assertTrue(hasattr(self.form, "submit_changes"))

    def test_should_change_name_field_is_string_field(self):
        self.assertIsInstance(self.form.change_name, StringField)

    def test_should_change_password_field_is_password_field(self):
        self.assertIsInstance(self.form.change_password, PasswordField)

    def test_should_change_avatar_field_is_file_field(self):
        self.assertIsInstance(self.form.change_avatar, FileField)

    def test_should_change_background_field_is_file_field(self):
        self.assertIsInstance(self.form.change_background, FileField)

    def test_should_channel_info_field_is_string_field(self):
        self.assertIsInstance(self.form.channel_info, StringField)

    def test_should_current_password_field_is_password_field(self):
        self.assertIsInstance(self.form.current_password, PasswordField)

    def test_should_submit_changes_password_is_submit_field(self):
        self.assertIsInstance(self.form.submit_changes, SubmitField)


class TestAddCommentForm(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context():
            self.form = AddCommentForm()

    def tearDown(self):
        del self.form

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.form, "message"))
        self.assertTrue(hasattr(self.form, "submit"))

    def test_should_message_field_is_string_field(self):
        self.assertIsInstance(self.form.message, StringField)

    def test_should_submit_field_is_string_field(self):
        self.assertIsInstance(self.form.submit, SubmitField)


class TestAddRoomForm(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context():
            self.form = AddRoomForm()

    def tearDown(self):
        del self.form

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.form, "token"))
        self.assertTrue(hasattr(self.form, "submit"))

    def test_should_token_field_is_string_field(self):
        self.assertIsInstance(self.form.token, StringField)

    def test_should_submit_field_is_string_field(self):
        self.assertIsInstance(self.form.submit, SubmitField)


class TestJoinForm(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context():
            self.form = JoinForm()

    def tearDown(self):
        del self.form

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.form, "token"))
        self.assertTrue(hasattr(self.form, "submit"))

    def test_should_token_field_is_string_field(self):
        self.assertIsInstance(self.form.token, StringField)

    def test_should_submit_field_is_string_field(self):
        self.assertIsInstance(self.form.submit, SubmitField)


class TestUploadVideoForm(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context():
            self.form = UploadVideoForm()

    def tearDown(self):
        del self.form

    def test_should_has_need_fields(self):
        self.assertTrue(hasattr(self.form, "title"))
        self.assertTrue(hasattr(self.form, "video"))
        # self.assertTrue(hasattr(self.form, "geotag_is_needed"))
        self.assertTrue(hasattr(self.form, "geotag_data"))
        self.assertTrue(hasattr(self.form, "submit"))

    def test_should_token_field_is_string_field(self):
        self.assertIsInstance(self.form.title, StringField)

    def test_should_video_field_is_file_field(self):
        self.assertIsInstance(self.form.video, FileField)

    # def test_should_geotag_is_needed_field_is_boolean_field(self):
    #     self.assertIsInstance(self.form.geotag_is_needed, BooleanField)

    def test_should_submit_field_is_string_field(self):
        self.assertIsInstance(self.form.submit, SubmitField)
