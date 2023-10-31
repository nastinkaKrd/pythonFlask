from flask import render_template, request, make_response, redirect, url_for, session, flash
import platform
from datetime import datetime, timedelta
from app import app
import json
from .forms import LoginForm, LogoutForm, ChangePasswordForm, AddCookieForm, DeleteCookieForm, DeleteAllCookiesForm

my_soft_skills = ["communication", "hard-working", "polite"]

my_hard_skills = ["Java", "Spring", "OOD", "Rest api", "MySql", "Postgresql", "Python", "Php", "C++", "JavaScript"]

cookies = []

nav_links = [
    {"text": "Home page", "url": "home"},
    {"text": "About me", "url": "about"},
    {"text": "My soft skills", "url": "soft_skills"},
    {"text": "My hard skills", "url": "hard_skills"},
    {"text": "Form page", "url": "login"},
]

@app.route('/')
def home():
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("home.html", os_info=os_info, user_agent_info=user_agent_info, current_time=current_time, nav_links=nav_links)


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

