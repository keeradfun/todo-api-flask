# apps.shared.models
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from sqlalchemy import text

db = SQLAlchemy()


def database_init(app):
    # database config
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{}:{}@{}/{}".format(config(
        "DB_USERNAME"), config("DB_PASSWORD"), config("DB_HOST"), config("DB_NAME"), echo=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initializing db
    db.init_app(app)

    # checking the connection
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("😎😎😎 DB Connection successful 😎😎😎")
        except Exception as e:
            print("😫 DB Connection failed! ERROR : ", e)

    # creating tables
    with app.app_context():
        try:
            from app.user import models
            from app.tasks import models
            db.create_all()
            print("😎😎😎 Table Creation successful 😎😎😎")
        except Exception as e:
            print("\n 😫 Table Creation Failed")
