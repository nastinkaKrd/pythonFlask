from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api, reqparse, abort
from marshmallow import Schema, fields
from ..auth.model import db, User

api_todo_br3 = Blueprint("api_todo_br3", __name__)
api = Api(api_todo_br3)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User is not found")
        serialized_user = user_schema.dump(user)
        return make_response(jsonify(serialized_user), 200)

    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be blank")
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank")
        args = parser.parse_args(strict=True)
        username = args.get('username')
        email = args.get('email')
        if not (username or email):
            abort(400, message="Write all args")
        user.username = username
        user.email = email
        db.session.commit()
        serialized_user = user_schema.dump(user)
        return make_response(jsonify(serialized_user), 200)

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 204


class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        serialized_users = users_schema.dump(users)
        return make_response(jsonify(serialized_users), 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be blank")
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        args = parser.parse_args(strict=True)
        username = args.get('username')
        email = args.get('email')
        password = args.get('password')
        if not (username or email or password):
            abort(400, message="Write all args")
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        serialized_user = user_schema.dump(new_user)
        return make_response(jsonify(serialized_user), 201)


api.add_resource(UserResource, '/account/users/<int:user_id>')
api.add_resource(UsersResource, '/account/users')

