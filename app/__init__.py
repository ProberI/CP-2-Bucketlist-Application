from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

app = Flask(__name__)
databases = SQLAlchemy(app)


def EnvironmentName(environ):
    app.config.from_object(app_config[environ])


EnvironmentName('TestingConfig')
