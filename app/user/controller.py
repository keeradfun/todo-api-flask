from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from .validation import RegisterSchema, LoginSchema, NewPasswordSchema
from marshmallow import ValidationError
from .models import User
from flask_jwt_extended import create_access_token, jwt_required
from .serializer import UserSchema
from flask_jwt_extended import current_user


class UserRegister(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            validated_data = RegisterSchema().load(data=json_data)
            if validated_data:
                new_user = User.create_user(
                    username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
                return {
                    "status": 200,
                    "message": new_user,
                    "code": "OK"
                }, 200
        except ValidationError as err:
            return {
                "status": 400,
                "message": err.messages,
                "code": "BAD_REQUEST"
            }, 400


class UserLogin(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            validated_data = LoginSchema().load(data=json_data)
            if validated_data:
                authenticate = User.authenticate_user(
                    email=validated_data['email'], password=validated_data['password'])
                if authenticate:
                    access_token = create_access_token(
                        identity=authenticate)
                    return {
                        "status": 200,
                        "data": {
                            "token": access_token
                        },
                        "code": "OK"
                    }, 200
                else:
                    return {
                        "status": 403,
                        "message": "Forbidden",
                        "code": "Forbidden"
                    }, 403

            else:
                return {
                    "status": 404,
                    "message": "Oops something went wrong",
                    "code": "OK"
                }, 404
        except ValidationError as err:
            return {
                "status": 400,
                "message": err.messages,
                "code": "BAD_REQUEST"
            }, 400


class UserManager(Resource):
    @jwt_required()
    def get(self):
        if current_user:
            serialized_user = UserSchema().dump(current_user)
            return {
                "status": 200,
                "data": {
                    "user": serialized_user
                },
                "code": "OK"
            }, 200
        else:
            return {
                "status": 400,
                "message": "Invalid user id",
                "code": "BAD_REQUEST"
            }, 400


class PasswordUpdate(Resource):
    @jwt_required()
    def post(self):
        try:
            if current_user:
                json_data = request.get_json(force=True)
                print(json_data)
                validated_data = NewPasswordSchema().load(data=json_data)
                if current_user:
                    new_password = User.update_password(
                        current_user.id, password=validated_data['password'])
                    if new_password:
                        return {
                            "status": 200,
                            "message": "successfully changed the password",
                            "code": "OK"
                        }, 200
                    else:
                        return {
                            "status": 400,
                            "message": "failed to change the password",
                            "code": "BAD_REQUEST"
                        }, 400
                else:
                    return {
                        "status": 404,
                        "message": "Oops something went wrong",
                        "code": "OK"
                    }, 404
        except ValidationError as err:
            return {
                "status": 400,
                "message": err.messages,
                "code": "BAD_REQUEST"
            }, 400
