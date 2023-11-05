from flask_wtf import FlaskForm
from app import models
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp


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


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")


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


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("New password", validators=[
        DataRequired(message="This field is required and must be between 4 and 10 characters long"),
        Length(min=4, max=10)
    ])
    submit = SubmitField("Change password")


class ItemForm(FlaskForm):
    title = StringField('Enter title here')
    description = StringField('Enter description here')
    submit = SubmitField('Add Item')


class FeedbackForm(FlaskForm):
    username = StringField('Enter username here')
    feedback = StringField('Enter feedback here')
    submit = SubmitField('Add feedback')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = FileField('Profile Image')
    submit = SubmitField('Add User')


class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete User')


class ChangeUserForm(FlaskForm):
    password = PasswordField('New password', validators=[DataRequired()])
    submit = SubmitField('Update User')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=14, message="Must be between 4 and 14 characters"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores')
    ])
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")])
    image = FileField('Profile Image')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if models.User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


    def validate_username(self, field):
        if models.User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm2(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
