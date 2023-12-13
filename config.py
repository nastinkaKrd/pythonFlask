from flask_jwt_extended import JWTManager
from flask_wtf import CSRFProtect
from flask import Flask
from os import environ, path

basedir = path.abspath(path.dirname(__file__))

app = Flask(__name__)
csrf = CSRFProtect(app)


class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret'
    FLASK_SECRET = SECRET_KEY
    JWT_SECRET_KEY = SECRET_KEY


class LocalConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


csrf.init_app(app)

config = {
    'local': LocalConfig,
    'test': TestConfig
}
