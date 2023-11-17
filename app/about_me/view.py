from flask import render_template
from . import about

my_soft_skills = ["communication", "hard-working", "polite"]

my_hard_skills = ["Java", "Spring", "OOD", "Rest api", "MySql", "Postgresql", "Python", "Php", "C++", "JavaScript"]


@about.route('/about')
def about_page():
    return render_template("about.html")


@about.route('/soft_skills', defaults={'idx': None})
@about.route('/soft_skills/<int:idx>')
def soft_skills(idx):
    if idx is None:
        return render_template("soft-skills.html", soft_skills=my_soft_skills)
    elif 0 < idx <= len(my_soft_skills):
        return render_template("skill.html", skill=my_soft_skills[idx-1], index=idx, soft_skills=my_soft_skills)
    else:
        return "Skill not found"


@about.route('/hard_skills', defaults={'idx': None})
@about.route('/hard_skills/<int:idx>')
def hard_skills(idx):
    if idx is None:
        return render_template("hard-skills.html", hard_skills=my_hard_skills)
    elif 0 < idx <= len(my_hard_skills):
        return render_template("skill.html", skill=my_hard_skills[idx-1], index=idx, hard_skills=my_hard_skills)
    else:
        return "Skill not found"
