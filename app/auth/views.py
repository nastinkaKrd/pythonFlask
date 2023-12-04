import os
import time
from flask_login import current_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_login import login_user
from PIL import Image
from .forms import (RegistrationForm, ChangeUserPassword, UpdateAccountForm, LoginForm2, UserForm, ChangeUserForm,
                    DeleteUserForm)
from .model import db, User
from werkzeug.utils import secure_filename
from . import auth
from app import create_app


@auth.route('/change-user-password', methods=['GET', 'POST'])
@login_required
def change_user_password():
    form = ChangeUserPassword()
    if form.validate_on_submit() or request.method == 'POST':
        old_password = form.old_password.data
        new_password = form.password.data
        user = User.query.filter_by(email=current_user.email).first()
        if user.password == old_password:
            user.password = new_password
            db.session.commit()
        return redirect(url_for("auth.my_profile"))
    return render_template('change_password.html', form=form)


@auth.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response


@auth.route('/my_profile', methods=['GET', 'POST'])
@login_required
def my_profile():
    app = create_app()
    form = UpdateAccountForm()
    if form.validate_on_submit() or request.method == 'POST':
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        profile_image = form.image.data
        if profile_image:
            filename = secure_filename(profile_image.filename)
            unique_filename = f"{current_user.username}_{int(time.time())}_{filename}.jpg"
            image = Image.open(profile_image)
            resized_image = image.resize((150, 150))
            resized_file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], unique_filename)
            resized_image.save(resized_file_path)
            profile_image_path = f'static/images/{unique_filename}'
            current_user.image_file = profile_image_path
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.my_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('my_profile.html', form=form)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    app = create_app()
    if current_user.is_authenticated:
        return redirect(url_for('appb.base'))
    form = RegistrationForm()
    if form.validate_on_submit() or request.method == 'POST':
        new_username = form.username.data
        new_email = form.email.data
        new_password = form.password.data
        profile_image = form.image.data
        if profile_image:
            filename = secure_filename(profile_image.filename)
            unique_filename = f"{new_username}_{int(time.time())}_{filename}.jpg"
            image = Image.open(profile_image)
            resized_image = image.resize((150, 150))
            resized_file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], unique_filename)
            resized_image.save(resized_file_path)
            profile_image_path = f'static/images/{unique_filename}'
        else:
            profile_image_path = 'static/images/my_photo.jpg'

        if new_username and new_email and new_password:
            user = User(username=new_username, email=new_email, image_file=profile_image_path)
            user.set_password(new_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', category='success')
            return redirect(url_for("appb.base"))
        return redirect(url_for('auth.login2'))
    return render_template('registr.html', form=form)


@auth.route("/login3", methods=['GET', 'POST'])
def login3():
    if current_user.is_authenticated:
        return redirect(url_for('auth.choice'))
    form = LoginForm2()
    if form.validate_on_submit() or request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember.data)
        flash('You have been logged in!', category='success')
        return redirect(url_for('appb.base'))
    return render_template('login2.html', form=form)


@auth.route("/choice")
def choice():
    return render_template('choice.html')


@auth.route("/logout-new")
def logout_new():
    logout_user()
    flash("You have been logged out", category='success')
    return redirect(url_for('appb.base'))


@auth.route('/user', methods=['GET', 'POST'])
def user():
    app = create_app()
    form = UserForm()
    del_form = DeleteUserForm()
    change_form = ChangeUserForm()
    users = User.query.all()
    users_amount = User.query.count()

    if form.validate_on_submit():
        new_username = form.username.data
        new_email = form.email.data
        new_password = form.password.data
        profile_image = form.image.data

        if profile_image:
            filename = secure_filename(profile_image.filename)
            unique_filename = f"{new_username}_{int(time.time())}_{filename}.jpg"
            file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], unique_filename)
            profile_image.save(file_path)

            profile_image_path = f'static/images/{unique_filename}'
        else:
            profile_image_path = 'static/images/my_photo.jpg'

        if new_username and new_email and new_password:
            user = User(username=new_username, email=new_email, image_file=profile_image_path)
            user.set_password(new_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.user"))

    if del_form.validate_on_submit():
        user_to_delete = User.query.filter_by(id=2).first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
        return redirect(url_for("auth.user"))

    if change_form.validate_on_submit():
        new_password = request.form.get('new_password')
        user_to_update = User.query.filter_by(id=1).first()

        if user_to_update:
            user_to_update.password = new_password
            db.session.commit()
        return redirect(url_for("user"))

    return render_template('users.html', users=users, users_amount=users_amount, form=form, del_form=del_form,
                           change_form=change_form)
