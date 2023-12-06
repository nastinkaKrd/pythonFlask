import unittest
from flask_testing import TestCase
from app import create_test


class FlaskAppbTestCase(TestCase):

    def create_app(self):
        app = create_test()
        return app

    def test_home_route(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home page', response.data)

    def test_base_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Base page', response.data)


if __name__ == '__main__':
    unittest.main()
