from app import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jwt = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
