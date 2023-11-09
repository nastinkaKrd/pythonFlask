import os
import time
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, request, make_response, redirect, url_for, session, flash
import platform
from datetime import datetime, timedelta
from flask_login import login_user
from PIL import Image
from app import app
import json
from .forms import LoginForm, RegistrationForm, ChangeUserPassword, UpdateAccountForm, LogoutForm, LoginForm2, ChangePasswordForm, \
    AddCookieForm, DeleteCookieForm, DeleteAllCookiesForm, ItemForm, FeedbackForm, UserForm, ChangeUserForm, \
    DeleteUserForm
from .models import Todo, db, Feedback, User
from werkzeug.utils import secure_filename

my_soft_skills = ["communication", "hard-working", "polite"]

my_hard_skills = ["Java", "Spring", "OOD", "Rest api", "MySql", "Postgresql", "Python", "Php", "C++", "JavaScript"]

cookies = []

nav_links = [
    {"text": "Home page", "url": "home"},
    {"text": "About me", "url": "about"},
    {"text": "My soft skills", "url": "soft_skills"},
    {"text": "My hard skills", "url": "hard_skills"},
    {"text": "Form page", "url": "login"},
    {"text": "TODO page", "url": "todo"},
    {"text": "Feedback page", "url": "feedback"},
    {"text": "User page", "url": "user"},
    {"text": "Register", "url": "register"},
    {"text": "Login3", "url": "login3"},
    {"text": "Logout new", "url": "logout_new"},
    {"text": "Choice", "url": "choice"}
]


@app.route('/change-user-password', methods=['GET', 'POST'])
@login_required
def change_user_password():
    form = ChangeUserPassword()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.password.data
        user = User.query.filter_by(email=current_user.email).first()
        if user.password == old_password:
            user.password = new_password
            db.session.commit()
        return redirect(url_for("my_profile"))
    return render_template('change_password.html', form=form)


@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response


@app.route('/my_profile', methods=['GET', 'POST'])
@login_required
def my_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
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
        else:
            profile_image_path = current_user.image_file
        current_user.image_file = profile_image_path
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('my_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('my_profile.html', user=current_user, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = RegistrationForm()
    if form.validate_on_submit():
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
            return redirect(url_for("base"))
        return redirect(url_for('login2'))
    return render_template('registr.html', form=form)


@app.route("/login3", methods=['GET', 'POST'])
def login3():
    if current_user.is_authenticated:
        return redirect(url_for('choice'))
    form = LoginForm2()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember.data)
        flash('You have been logged in!', category='success')
        return redirect(url_for('base'))
    return render_template('login2.html', form=form)


@app.route("/choice")
def choice():
    return render_template('choice.html')


@app.route("/logout-new")
def logout_new():
    logout_user()
    flash("You have been logged out", category='success')
    return redirect(url_for('base'))


@app.route("/login2", methods=['GET', 'POST'])
def login2():
    form = LoginForm2()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if form.remember.data:
                session["email"] = form.email.data
                session["password"] = form.password.data
                flash("You are logged in successfully and remembered", category="success")
            else:
                flash('You have been logged in!', category='success')
            return redirect(url_for('base'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login2.html', form=form)


@app.route('/user', methods=['GET', 'POST'])
def user():
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
            return redirect(url_for("user"))

    if del_form.validate_on_submit():
        user_to_delete = User.query.filter_by(id=2).first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
        return redirect(url_for("user"))

    if change_form.validate_on_submit():
        new_password = request.form.get('new_password')
        user_to_update = User.query.filter_by(id=1).first()

        if user_to_update:
            user_to_update.password = new_password
            db.session.commit()
        return redirect(url_for("user"))

    return render_template('users.html', users=users, users_amount=users_amount, form=form, del_form=del_form,
                           change_form=change_form)


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    feedbacks = db.session.query(Feedback).all()
    if form.validate_on_submit():
        username = form.username.data
        feedback_msg = form.feedback.data
        if username and feedback_msg:
            db.session.add(Feedback(username=username, feedback=feedback_msg))
            db.session.commit()
            flash("Feedback is added!", category="success")
        else:
            flash("Feedback isn't added!", category="danger")
        return redirect(url_for("feedback"))
    return render_template('feedback.html', feedbacks=feedbacks, form=form)


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = ItemForm()
    todo_list = db.session.query(Todo).all()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("todo"))

    return render_template('todo.html', todo_list=todo_list, form=form)


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route('/')
def base():
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("base.html", os_info=os_info, user_agent_info=user_agent_info, current_time=current_time,
                           nav_links=nav_links)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/soft_skills', defaults={'idx': None})
@app.route('/soft_skills/<int:idx>')
def soft_skills(idx):
    if idx is None:
        return render_template("soft-skills.html", soft_skills=my_soft_skills)
    elif 0 <= idx <= len(my_soft_skills):
        return render_template("skill.html", skill=my_soft_skills[idx - 1], index=idx, soft_skills=my_soft_skills)
    else:
        return "Skill not found"


@app.route('/hard_skills', defaults={'idx': None})
@app.route('/hard_skills/<int:idx>')
def hard_skills(idx):
    if idx is None:
        return render_template("hard-skills.html", hard_skills=my_hard_skills)
    elif 0 <= idx <= len(my_hard_skills):
        return render_template("skill.html", skill=my_hard_skills[idx - 1], index=idx, hard_skills=my_hard_skills)
    else:
        return "Skill not found"


@app.route('/info')
def info():
    user = session.get('username')
    form_logout = LogoutForm()
    form_change_password = ChangePasswordForm()
    form_add_cookie = AddCookieForm()
    form_delete_cookie = DeleteCookieForm()
    form_delete_all_cookies = DeleteAllCookiesForm()
    return render_template("info.html", cookies=cookies, name=user, form_add_cookie=form_add_cookie,
                           form_delete_cookie=form_delete_cookie, form_delete_all_cookies=form_delete_all_cookies,
                           form_logout=form_logout,
                           form_change_password=form_change_password)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username')
    session.pop('password')
    return redirect(url_for("login"))


@app.route('/add_cookie', methods=["POST"])
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    expiration = request.form.get('expiration')
    if key and value and expiration:
        expiration = int(expiration)
        expiration_time = datetime.now() + timedelta(seconds=expiration)

        new_cookie = {
            'key': key,
            'value': value,
            'expiration': expiration,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        cookies.append(new_cookie)
        response = make_response(redirect(url_for("info")))
        response.set_cookie(key, value, expires=expiration_time)
        flash("Cookie is added.", category="success")
        return response
    else:
        flash("Error: Cookie isn't added.", category="danger")
        return redirect(url_for("info"))


@app.route('/delete_cookie', methods=["POST"])
def delete_cookie():
    delete_key = request.form.get('key')
    for cookie in cookies:
        if cookie['key'] == delete_key:
            cookies.remove(cookie)
            response = make_response(redirect(url_for("info")))
            response.delete_cookie(delete_key)
            flash("Cookie is deleted.", category="success")
            return response
    flash("Error: Cookie is not deleted.", category="danger")
    return redirect(url_for("info"))


@app.route('/delete_all_cookies', methods=["POST"])
def delete_all_cookies():
    for cookie in cookies:
        response = make_response(redirect(url_for("info")))
        response.delete_cookie(cookie['key'])
    cookies.clear()
    flash("Cookies are deleted.", category="success")
    return response


@app.route('/change_password', methods=['POST'])
def change_password():
    user = session.get('username')
    if user:
        new_password = request.form.get('new_password')
        if new_password:
            session['password'] = new_password
            flash("Password changed successfully.", category="success")
        else:
            flash("Error: Password cannot be empty.", category="danger")

        return redirect(url_for("info"))

    return redirect(url_for("login"))


@app.route("/login-form", methods=['GET', 'POST'])
def login():
    form_main = LoginForm()
    if request.method == "POST":
        username = form_main.username.data
        password = form_main.password.data
        remember = form_main.remember.data
        if session.get('password') and session.get("username"):
            if session.get('password') == password and session.get("username") == username:
                return redirect(url_for("info"))
        else:
            with open('app\\dataJson.json', 'r') as json_file:
                data = json.load(json_file)
            if 'name' in data and 'password' in data:
                if data['name'] == username and data['password'] == password:
                    if remember:
                        session["username"] = username
                        session["password"] = password
                        flash("You are logged in successfully and remembered", category="success")
                    else:
                        flash("You are logged in successfully", category="success")
                    return redirect(url_for("info"))
                else:
                    flash("You aren't logged in", category="danger")

    return render_template("login.html", form_main=form_main)
