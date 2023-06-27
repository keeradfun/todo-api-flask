from flask_jwt_extended import JWTManager
from decouple import config


def jwt_init(app):
    app.config["JWT_SECRET_KEY"] = config("SECRET")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 1800
    jwt = JWTManager(app)
    with app.app_context():
        from app.user.models import User

        @jwt.user_identity_loader
        def user_identity_lookup(user):
            return user.id

        @jwt.user_lookup_loader
        def user_lookup_callback(_jwt_header, jwt_data):
            user = User.findone(id=jwt_data["sub"])
            return user
