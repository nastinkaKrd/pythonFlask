from flask_wtf import CSRFProtect
from app import app


app.secret_key = b"secret"
csrf = CSRFProtect(app)
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
