from flask import render_template, request, make_response, redirect, url_for, session
import platform
from datetime import datetime, timedelta
from app import app
import json

my_soft_skills = ["communication", "hard-working", "polite"]

my_hard_skills = ["Java", "Spring", "OOD", "Rest api", "MySql", "Postgresql", "Python", "Php", "C++", "JavaScript"]

cookies = []


@app.route('/')
def home():
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("home.html", os_info=os_info, user_agent_info=user_agent_info, current_time=current_time)


@app.route('/about')
def about():
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("about.html", os_info=os_info, user_agent_info=user_agent_info, current_time=current_time)


@app.route('/soft_skills', defaults={'idx': None})
@app.route('/soft_skills/<int:idx>')
def soft_skills(idx):
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if idx is None:
        return render_template("soft-skills.html", soft_skills=my_soft_skills, os_info=os_info,
                               user_agent_info=user_agent_info, current_time=current_time)
    elif 0 <= idx <= len(my_soft_skills):
        return render_template("skill.html", skill=my_soft_skills[idx - 1], index=idx, hard_skills=my_hard_skills,
                               os_info=os_info, user_agent_info=user_agent_info, current_time=current_time)
    else:
        return "Skill not found"


@app.route('/hard_skills', defaults={'idx': None})
@app.route('/hard_skills/<int:idx>')
def hard_skills(idx):
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if idx is None:
        return render_template("hard-skills.html", hard_skills=my_hard_skills, os_info=os_info,
                               user_agent_info=user_agent_info, current_time=current_time)
    elif 0 <= idx <= len(my_hard_skills):
        return render_template("skill.html", skill=my_hard_skills[idx - 1], index=idx, hard_skills=my_hard_skills,
                               os_info=os_info, user_agent_info=user_agent_info, current_time=current_time)
    else:
        return "Skill not found"


@app.route('/form')
def form():
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("login.html", os_info=os_info, user_agent_info=user_agent_info, current_time=current_time)


@app.route('/form/hi', methods=["GET", "POST"])
def form_hi():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        with open('app\\dataJson.json', 'r') as json_file:
            data = json.load(json_file)

        if 'name' in data and 'password' in data:
            if session.get('password'):
                if session.get('password') == password:
                    return redirect(url_for("info"))
            elif data['name'] == name and data['password'] == password:
                session["username"] = name
                return redirect(url_for("info"))
    return redirect(url_for("form"))


@app.route('/info')
def info():
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = session.get('username')
    if user:
        return render_template("info.html", cookies=cookies, name=user, os_info=os_info,
                               user_agent_info=user_agent_info, current_time=current_time, msgA=session.get('msgA'),
                               msgD=session.get('msgD'), msgDA=session.get('msgDA'), msg_password=session.get('msg_password'))
    else:
        return redirect(url_for("form"))


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username')
    session.pop('password')
    return redirect(url_for("form"))


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
        session['msgA'] = "Cookie is added"
        return response
    else:
        session['msgA'] = "Error"
        return redirect(url_for("info"))


@app.route('/delete_cookie', methods=["POST"])
def delete_cookie():
    delete_key = request.form.get('delete_key')
    for cookie in cookies:
        if cookie['key'] == delete_key:
            cookies.remove(cookie)
            response = make_response(redirect(url_for("info")))
            response.delete_cookie(delete_key)
            session['msgD'] = "Cookie is deleted"
            return response
    session['msgD'] = "Error"
    return redirect(url_for("info"))


@app.route('/delete_all_cookies', methods=["POST"])
def delete_all_cookies():
    for cookie in cookies:
        response = make_response(redirect(url_for("info")))
        response.delete_cookie(cookie['key'])
    cookies.clear()
    session['msgDA'] = "Cookies are deleted"
    return response


@app.route('/change_password', methods=['POST'])
def change_password():
    user = session.get('username')
    if user:
        new_password = request.form.get('new_password')

        if new_password:
            session['password'] = new_password
            session['msg_password'] = "Password changed successfully."
        else:
            session['msg_password'] = "Error: Password cannot be empty."

        return redirect(url_for("info"))

    return redirect(url_for("form"))
