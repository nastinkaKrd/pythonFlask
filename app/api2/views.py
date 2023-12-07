from flask import request, jsonify

from ..todo.model import Todo, db
from . import api_todo_br2


@api_todo_br2.route('/todo-api2', methods=['GET'])
def get():
    todo_list = Todo.query.all()
    if todo_list:
        return {
            'todo_list': [{'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete}
                          for todo in todo_list]}
    else:
        return {
            "message": "todo is not found"
        }, 404


@api_todo_br2.route('/todo-api2/post', methods=['POST'])
def post():
    new_data = request.get_json()
    title = new_data.get('title')
    description = new_data.get('description')
    if title and description:
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        todo = Todo.query.filter_by(title=new_todo.title).first()
        return jsonify(
            {
                "message": "todo was added",
                "title": todo.title
            }), 201
    else:
        return {
            "message": "no input data provided"
        }, 400


@api_todo_br2.route("/todo-api2/<int:todo_id>", methods=['GET'])
def get_by_id(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        return jsonify(
            {
                "message": "todo is found",
                "title": todo.title
            }), 200
    else:
        return {
            "message": "todo is not found"
        }, 404


@api_todo_br2.route("/todo-api2/<int:todo_id>", methods=['DELETE'])
def delete_by_id(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return {
                    "message": "todo is found and deleted"
                }, 204
    else:
        return {
            "message": "todo is not found"
        }, 404


@api_todo_br2.route("/update-complete-api/<int:todo_id>", methods=['PUT'])
def update_complete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
        todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
        return jsonify(
            {
                "message": "todo is found",
                "title": todo.title,
                "description": todo.description,
                "complete": todo.complete
            }), 200
    else:
        return {
            "message": "todo is not found"
        }, 404


@api_todo_br2.route("/update-api/<int:todo_id>", methods=['PUT'])
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        new_data = request.get_json()
        title = new_data.get('title')
        description = new_data.get('description')
        if title and description:
            todo.title = title
            todo.description = description
            db.session.commit()
            todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
        return jsonify(
            {
                "message": "todo is found",
                "title": todo.title,
                "description": todo.description,
                "complete": todo.complete
            }), 200
    else:
        return {
            "message": "todo is not found"
        }, 404



