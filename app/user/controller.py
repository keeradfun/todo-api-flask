from flask import request, abort
from flask_restful import Resource
from .validation import UserCreateValidation, UserLoginValidation, NewPasswordValidation, UserUpdateValidation
from marshmallow import ValidationError
from .models import User
from flask_jwt_extended import create_access_token, jwt_required, current_user
from .serializer import UserSerializer
from app.user.utils import hash_password


class UsersManager(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            if json_data:
                validated_data = UserCreateValidation().load(data=json_data)
                if validated_data:
                    user = User(email=validated_data['email'],
                                username=validated_data['username'],
                                password=hash_password(
                                    validated_data['password'])
                                )
                    user.create()

                    return {
                        "status": True,
                        "user": UserSerializer().dump(user)
                    }, 200

        except ValidationError as err:
            return {
                "status": False,
                "message": err.messages
            }, 400

    @jwt_required()
    def get(self):
        try:
            users = User.findall()
            if users:
                serialized_data = []
                for user in users:
                    serialized_data.append(UserSerializer().dump(user))

                return {
                    "status": True,
                    "users": serialized_data
                }, 200
        except Exception as e:
            abort(422)

    @jwt_required()
    def put(self):
        try:
            json_data = request.get_json(force=True)
            if json_data:
                validated_data = NewPasswordValidation().load(data=json_data)
                if validated_data:
                    User.update_password(
                        id=current_user.id, password=validated_data['password'])

                    return {
                        "status": True,
                        "message": "success"
                    }, 200

        except ValidationError as err:
            return {
                "status": False,
                "message": err.messages
            }, 400


class UserManager(Resource):
    @jwt_required()
    def get(self, id):
        try:
            user = User.findone(id=id)
            if user:
                serialized_user = UserSerializer().dump(user)
                return {
                    "status": True,
                    "user": serialized_user
                }
            else:
                return {
                    "status": False,
                    "message": "user not found"
                }, 400
        except:
            abort(422)

    @jwt_required()
    def put(self, id):
        try:
            if not current_user.superadmin:
                return {
                    "status": False,
                    "message": "Forbidden"
                }, 403
            json_data = request.get_json(force=True)
            if json_data:
                validated_data = UserUpdateValidation().load(data=json_data)
                if validated_data:
                    user = User.update(id, validated_data)
                    if user:
                        user = User.findone(id=id)
                        return {
                            "status": True,
                            "user": UserSerializer().dump(user)
                        }, 200
                    else:
                        return {
                            "status": False,
                            "message": "Invalid user id"
                        }, 400

        except ValidationError as err:
            return {
                "status": False,
                "message": err.messages
            }, 400

    @jwt_required()
    def delete(self, id):
        try:
            if not current_user.superadmin:
                return {
                    "status": False,
                    "message": "FORBIDDEN"
                }, 403
            if current_user.id == id:
                return {
                    "status": False,
                    "message": "can not delete your self"
                }, 400
            user = User.delete(id=id)
            if user:
                return {
                    "status": True,
                    "message": "success"
                }, 200
            else:
                return {
                    "status": False,
                    "message": "Can not delete"
                }, 400
        except:
            abort(422)


class LoginManager(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            if json_data:
                validated_data = UserLoginValidation().load(data=json_data)
                if validated_data:
                    user = User.authenticate_user(
                        email=validated_data['email'], password=validated_data['password'])
                    if user:
                        return {
                            "status": True,
                            "user": UserSerializer().dump(user),
                            "token": create_access_token(identity=user)
                        }, 200

                    else:
                        return {
                            "status": False,
                            "message": "Invalid email or password"
                        }, 400

        except ValidationError as err:
            return {
                "status": False,
                "message": err.messages
            }, 400

        except:
            return abort(422)
