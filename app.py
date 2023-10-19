from flask import Flask, render_template, request
import platform #os не підтримується на моїй операційній системі
from _datetime import datetime

app = Flask(__name__)

my_soft_skills = ["communication", "hard-working", "polite"]

my_hard_skills = ["Java", "Spring", "OOD", "Rest api", "MySql", "Postgresql", "Python", "Php", "C++", "JavaScript"]


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


if __name__ == '__main__':
    app.run()
