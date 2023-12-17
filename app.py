from flask_jwt_extended import JWTManager
from flask_restful_swagger_2 import Api as SwaggerApi

from app.accounts_api.vievs import UserResource, UsersResource

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    swagger_api = SwaggerApi(app)
    swagger_api.add_resource(UserResource, '/account/users/<int:user_id>')
    swagger_api.add_resource(UsersResource, '/account/users')
    JWTManager(app)
    app.run(debug=True)
