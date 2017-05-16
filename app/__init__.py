from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config


app = Flask(__name__)


def EnvironmentName(environ):
    app.config.from_object(app_config[environ])


EnvironmentName('DevelopmentEnviron')
databases = SQLAlchemy(app)
from app.v1 import bucketlist
