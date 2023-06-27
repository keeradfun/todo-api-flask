import os
from flask import Flask
from decouple import config
from sqlalchemy import text
from .database import db
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # db connection
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{}:{}@{}/{}".format(config(
        "DB_USERNAME"), config("DB_PASSWORD"), config("DB_HOST"), config("DB_NAME"), echo=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("😎😎😎\nDB Connection successful \n😎😎😎")
        except Exception as e:
            print("\n 😫DB Connection failed! ERROR : ", e)

    # cors settings
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.static_url_path = "/static"

    # jwt config
    app.config["JWT_SECRET_KEY"] = config("SECRET")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 1800
    jwt = JWTManager(app)

    # models import and creating tables
    from app.user import models
    from app.tasks import models
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("\n table creation  failed")

    # jwt context loader
    with app.app_context():
        from app.user.models import User

        @jwt.user_identity_loader
        def user_identity_lookup(user):
            return user.id

        @jwt.user_lookup_loader
        def user_lookup_callback(_jwt_header, jwt_data):
            user = User.findone(id=jwt_data["sub"])
            return user

    # importing api urls
    api = Api(app)
    ma = Marshmallow(app)
    from app.user.urls import define_urls as user_urls
    from app.tasks.urls import define_urls as task_urls
    with app.app_context():
        user_urls(api)
        task_urls(api)

    return app
