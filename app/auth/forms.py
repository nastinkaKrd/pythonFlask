from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from .model import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("New password", validators=[
        DataRequired(message="This field is required and must be between 4 and 10 characters long"),
        Length(min=4, max=10)
    ])
    submit = SubmitField("Change password")


class ChangeUserForm(FlaskForm):
    password = PasswordField('New password', validators=[DataRequired()])
    submit = SubmitField('Update User')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = FileField('Profile Image')
    submit = SubmitField('Add User')


class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete User')


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
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm2(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About Me', validators=[Length(max=140)])
    image = FileField('Update image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField()

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already taken. Please choose a different one.')


class ChangeUserPassword(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Update')
