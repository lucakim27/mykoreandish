import unittest
from backend import create_app
from backend.config.config import Config

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

class SetupTestCase(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        app = create_app(TestConfig)
        app.testing = True
        cls.app = app
        cls.client = app.test_client()
