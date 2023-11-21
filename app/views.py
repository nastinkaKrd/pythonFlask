from flask import render_template, request, Blueprint
import platform
from datetime import datetime


appb = Blueprint("appb", __name__, template_folder="templates")

nav_links = [
    {"text": "Home page", "url": "appb.home"},
    {"text": "About me", "url": "about.about_page"},
    {"text": "My soft skills", "url": "about.soft_skills"},
    {"text": "My hard skills", "url": "about.hard_skills"},
    {"text": "TODO page", "url": "todo_br.todo"},
    {"text": "Feedback page", "url": "feedback_br.feedback"},
    {"text": "User page", "url": "auth.user"},
    {"text": "Register", "url": "auth.register"},
    {"text": "Login3", "url": "auth.login3"},
    {"text": "Logout new", "url": "auth.logout_new"},
    {"text": "Choice", "url": "auth.choice"},
    {"text": "Cookie", "url": "cookie.login"},
    {"text": "Create post", "url": "post.create_post"},
    {"text": "Show posts", "url": "post.list_posts"},
    {"text": "Create category", "url": "post.create_category"},

]


@appb.route('/home')
def home():
    return render_template("other/home.html")


@appb.route('/')
def base():
    os_info = platform.platform()
    user_agent_info = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("other/base.html", os_info=os_info, user_agent_info=user_agent_info,
                           current_time=current_time, nav_links=nav_links)
