from flask import Blueprint

feedback_br = Blueprint("feedback_br", __name__, template_folder="templates/feedback")

from . import views
