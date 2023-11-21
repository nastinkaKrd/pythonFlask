from flask import Blueprint

post = Blueprint("post", __name__, template_folder="templates/post")


from . import views
