from app import db, login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    description = db.Column(db.String(300))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    feedback = db.Column(db.String(350))


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='static/images/my_photo')
    password = db.Column(db.String(60), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def repr(self):
        return f"User('{self.username}', '{self.email}')"
