import unittest

from flask import url_for
from flask_testing import TestCase
from app import create_app, db
from app.todo.model import Todo


class TestTodoBlueprint(TestCase):

    def create_app(self):
        app = create_app('test')
        return app

    def setUp(self):
        self.todo = Todo(title='Test Todo', description='Test description', complete=False)
        db.session.add(self.todo)
        db.session.commit()

    def tearDown(self):
        all_todos = db.session.query(Todo).all()
        for todo in all_todos:
            db.session.delete(todo)
        db.session.commit()

    def test_todo_get(self):
        response = self.client.get('/todo')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('todo.html')
        self.assertIn(b'Test Todo', response.data)

    def test_todo_post(self):
        data = {
            'title': 'Test Todo2',
            'description': 'Test description2'
        }
        with self.client:
            response = self.client.post(
                url_for('todo_br.todo'),
                data=data,
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<td>Test Todo2</td>', response.data)

    def test_todo_update(self):
        todo_id = self.todo.id
        with self.client:
            response = self.client.post(
                url_for('todo_br.update', todo_id=todo_id),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<div class="alert alert-success" role="alert">Completed</div>', response.data)

    def test_delete(self):
        with self.client:
            response = self.client.post(
                url_for('todo_br.delete', todo_id=self.todo.id),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            deleted_todo = db.session.query(Todo).filter_by(id=self.todo.id).first()
            self.assertIsNone(deleted_todo)


if __name__ == '__main__':
    unittest.main()
