from flask import Blueprint

dash = Blueprint('dash', __name__,static_url_path='')

from . import views
