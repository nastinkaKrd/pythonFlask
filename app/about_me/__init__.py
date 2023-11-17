from flask import Blueprint

about = Blueprint("about", __name__, template_folder="templates/about_me")


from . import view
