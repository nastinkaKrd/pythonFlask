from flask import Blueprint

api_todo_br2 = Blueprint("api_todo_br2", __name__)

from . import views
