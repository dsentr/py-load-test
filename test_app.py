import unittest
import app


class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_default(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_home(self):
        result = self.app.get('/home')
        self.assertEqual(result.status_code, 200)
