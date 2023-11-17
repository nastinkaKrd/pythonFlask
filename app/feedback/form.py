from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class FeedbackForm(FlaskForm):
    username = StringField('Enter username here')
    feedback = StringField('Enter feedback here')
    submit = SubmitField('Add feedback')
