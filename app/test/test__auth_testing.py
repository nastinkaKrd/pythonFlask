import unittest
from flask import url_for
from flask_login import current_user, login_user
from flask_testing import TestCase
from app import create_test, db
from app.auth.model import User


class TestAuthBlueprint(TestCase):

    def create_app(self):
        app = create_test()
        return app

    def setUp(self):
        self.user = User(username='testing_user', email='testing@example.com', password='test_password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        all_users = db.session.query(User).all()
        for user in all_users:
            db.session.delete(user)
        db.session.commit()

    def test_register(self):
        user_data = {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }
        with self.client:
            response = self.client.post(
                url_for('auth.register'),
                data=user_data,
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account created for TestUser!', response.data)
            new_user = db.session.query(User).filter_by(username='TestUser').first()
            self.assertIsNotNone(new_user)
            self.assertEqual(new_user.email, 'testuser@example.com')

    def test_register_get(self):
        response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registr.html')

    def test_login3(self):
        login_data = {
            'email': 'testing@example.com',
            'password': 'test_password',
            'remember': False
        }
        with self.client:
            response = self.client.post(
                url_for('auth.login3'),
                data=login_data,
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have been logged in!', response.data)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.email, 'testing@example.com')

    def test_login3_get(self):
        response = self.client.get(url_for('auth.login3'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('login2.html')

    def test_logout_new(self):
        login_user(self.user)
        with self.client:
            response = self.client.get(
                url_for('auth.logout_new'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have been logged out', response.data)
            self.assertFalse(current_user.is_authenticated)
            self.assertIsNone(current_user.get_id())

    def test_my_profile(self):
        login_user(self.user)
        update_data = {
            'username': 'Updated username',
            'email': 'updateduser@example.com',
            'about_me': 'Updated about me'
        }
        with self.client:
            response = self.client.post(
                url_for('auth.my_profile'),
                data=update_data,
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your account has been updated!', response.data)
            self.assertEqual(self.user.username, 'Updated username')
            self.assertEqual(self.user.email, 'updateduser@example.com')
            self.assertEqual(self.user.about_me, 'Updated about me')

    def test_about_get(self):
        login_user(self.user)
        response = self.client.get(url_for('auth.my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('my_profile.html')


if __name__ == '__main__':
    unittest.main()
