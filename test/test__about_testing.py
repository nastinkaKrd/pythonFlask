import unittest
from flask_testing import TestCase
from app import create_test


class TestAboutBlueprint(TestCase):

    def create_app(self):
        app = create_test()
        return app

    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('about.html')

    def test_soft_skills_route(self):
        response = self.client.get('/soft_skills')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('soft-skills.html')

    def test_soft_skills_with_index(self):
        response = self.client.get('/soft_skills/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('skill.html')
        self.assertIn(b'communication', response.data)

    def test_soft_skills_with_invalid_index(self):
        response = self.client.get('/soft_skills/10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Skill not found')

    def test_hard_skills_route(self):
        response = self.client.get('/hard_skills')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('hard-skills.html')

    def test_hard_skills_with_index(self):
        response = self.client.get('/hard_skills/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('skill.html')
        self.assertIn(b'Java', response.data)

    def test_hard_skills_with_invalid_index(self):
        response = self.client.get('/hard_skills/11')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Skill not found')


if __name__ == '__main__':
    unittest.main()
