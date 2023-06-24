from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from .validation import RegisterSchema,LoginSchema
from marshmallow import ValidationError
from .models import User
from flask_jwt_extended import create_access_token

class UserRegister(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            validated_data = RegisterSchema().load(data=json_data)
            if validated_data:
                new_user = User.create_user(username=validated_data['username'],email=validated_data['email'],password=validated_data['password'])
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
                authenticate = User.authenticate_user(email=validated_data['email'],password=validated_data['password'])
                if authenticate:
                    access_token = create_access_token(identity=authenticate.id)
                    return {
                        "status": 200,
                        "data":{
                            "token" : access_token
                        } ,
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
        

