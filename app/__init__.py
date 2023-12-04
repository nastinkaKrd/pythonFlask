from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='local'):
    app = Flask(__name__)
    app.config["UPLOADED_PHOTOS_DEST"] = "app/static/images/"
    app.config['STATIC_FOLDER'] = "app/static/images/"
    if config_name not in config:
        raise ValueError(f"Invalid configuration name: {config_name}")

    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login3'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from app.about_me import about
        from app.auth import auth
        from app.cookie import cookie
        from app.feedback import feedback_br
        from app.todo import todo_br
        from app.views import appb
        from app.post import post

        app.register_blueprint(about)
        app.register_blueprint(auth)
        app.register_blueprint(cookie)
        app.register_blueprint(feedback_br)
        app.register_blueprint(todo_br)
        app.register_blueprint(appb)
        app.register_blueprint(post)

    return app


def create_test(config_name='test'):
    app = Flask(__name__)
    app.config["UPLOADED_PHOTOS_DEST"] = "app/static/images/"
    app.config['STATIC_FOLDER'] = "app/static/images/"
    if config_name not in config:
        raise ValueError(f"Invalid configuration name: {config_name}")

    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login3'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from app.about_me import about
        from app.auth import auth
        from app.cookie import cookie
        from app.feedback import feedback_br
        from app.todo import todo_br
        from app.views import appb
        from app.post import post

        app.register_blueprint(about)
        app.register_blueprint(auth)
        app.register_blueprint(cookie)
        app.register_blueprint(feedback_br)
        app.register_blueprint(todo_br)
        app.register_blueprint(appb)
        app.register_blueprint(post)

    return app
