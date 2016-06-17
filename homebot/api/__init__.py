from flask import Blueprint

api_module = Blueprint('api_module',__name__,template_folder='templates',static_folder='static')

from . import views

