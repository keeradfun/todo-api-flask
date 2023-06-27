from flask_restful import Api
from app.user.urls import define_urls as user_urls
from app.tasks.urls import define_urls as task_urls


def api_init(app):
    api = Api(app)

    with app.app_context():
        user_urls(api)
        task_urls(api)
