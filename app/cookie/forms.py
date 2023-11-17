from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length


class AddCookieForm(FlaskForm):
    key = StringField("Key", validators=[
        DataRequired(message="This field is required")
    ])
    value = StringField("Value", validators=[
        DataRequired(message="This field is required")
    ])
    expiration = IntegerField("Value", validators=[
        DataRequired(message="This field is required")
    ])
    submit = SubmitField("Add cookie")


class DeleteCookieForm(FlaskForm):
    key = StringField("Key", validators=[
        DataRequired(message="This field is required")
    ])
    submit = SubmitField("Delete cookie")


class DeleteAllCookiesForm(FlaskForm):
    submit = SubmitField("Delete all cookies")


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("New password", validators=[
        DataRequired(message="This field is required and must be between 4 and 10 characters long"),
        Length(min=4, max=10)
    ])
    submit = SubmitField("Change password")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(message="This field is required"),
        Length(min=4, max=10)
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="This field is required and must be between 4 and 10 characters long"),
        Length(min=4, max=10)
    ])
    remember = BooleanField("Remember")
    submit = SubmitField("Sign in")




