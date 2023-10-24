from flask import Flask
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.secret_key = b"secret"
app.config['SECRET_KEY'] = 'secret'
csrf = CSRFProtect(app)


from app import views
