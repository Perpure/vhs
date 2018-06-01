# coding=utf-8
import unittest
import os
from web import app, db
from web.models import User, Video

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB_PATH = os.path.join(BASE_DIR, 'test.sqlite')


class TestVideoHandler(unittest.TestCase):
    pass