from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config


app = Flask(__name__)


def EnvironmentName(environ):
    '''Function to set config envirionment type'''
    app.config.from_object(app_config[environ])


EnvironmentName('DevelopmentEnviron')
databases = SQLAlchemy(app)  # Make databases models default to app context
from app.v1 import bucketlist
