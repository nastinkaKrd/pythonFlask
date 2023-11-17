from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ItemForm(FlaskForm):
    title = StringField('Enter title here')
    description = StringField('Enter description here')
    submit = SubmitField('Add Item')
