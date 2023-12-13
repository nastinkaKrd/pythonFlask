from flask_jwt_extended import JWTManager

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    JWTManager(app)
    app.run(debug=True)
