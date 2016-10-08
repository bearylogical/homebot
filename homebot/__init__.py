from flask import Flask
import os.path
import yaml
from flask.ext.sqlalchemy import SQLAlchemy


with open(os.path.dirname(__file__) + "/../config.yaml", "r") as ymlfile:
    settings = yaml.load(ymlfile)
from .api import api_module
from .dash.views import dash as dash_module

homebot =Flask(__name__)
homebot.config.update(
    DEBUG=settings['flask']['DEBUG'],
    CSRF_ENABLED=settings['flask']['CSRF_ENABLED'],
    SECRET_KEY=settings['flask']['SECRET_KEY'],
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.dirname(__file__) + "/../homebot.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=True
)

db = SQLAlchemy(homebot)

homebot.register_blueprint(api_module,url_prefix='/api')
homebot.register_blueprint(dash_module,url_prefix='/dash')
from homebot import models

db.create_all()  # In case user table doesn't exists already. Else remove it.

