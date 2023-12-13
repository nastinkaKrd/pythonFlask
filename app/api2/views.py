from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_login import login_user, current_user

from . import api_todo_br2
from .model import Token
from ..auth.model import User, bcrypt
from ..todo.model import Todo, db


@api_todo_br2.route('/todo-api2/refresh', methods=['POST'])
@jwt_required()
def refresh():
    new_access_token = create_access_token(identity=current_user.id)
    token = Token.query.filter_by(user_id=current_user.id).first()
    token.jwt = new_access_token
    db.session.commit()
    return jsonify(access_token=new_access_token), 200


@api_todo_br2.route('/todo-api2/revoke', methods=['DELETE'])
@jwt_required()
def revoke():
    token = Token.query.filter_by(user_id=current_user.id).first()
    db.session.delete(token)
    db.session.commit()
    return jsonify({"message": "Token revoked"}), 200


@api_todo_br2.route('/todo-api2/login', methods=['POST'])
def login():
    user_data = request.get_json()
    email = user_data.get('email')
    password = user_data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        new_token = Token(
            jwt=access_token,
            user_id=user.id
        )
        db.session.add(new_token)
        db.session.commit()
        login_user(user)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


@api_todo_br2.route('/todo-api2', methods=['GET'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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



