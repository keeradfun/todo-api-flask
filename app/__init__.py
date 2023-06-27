import os
from flask import Flask
from decouple import config
from .database import database_init
from .auth import jwt_init
from .api import api_init
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # cors settings
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.static_url_path = "/static"

    # db connection
    with app.app_context():
        database_init(app)
    # import JWT
        jwt_init(app)
    # importing api urls
        api_init(app)

    return app
