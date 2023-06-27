from .models import User
from marshmallow import Schema, fields, validate, ValidationError, validates, validates_schema
from flask_marshmallow import Marshmallow


class UserCreateValidation(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=3))
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @validates("email")
    def validate_email(self, value):
        if User.email_exist(email=value):
            raise ValidationError("Email already taken")

    @validates("username")
    def validate_username(self, value):
        if User.username_exist(username=value):
            raise ValidationError("Username already taken")


class UserLoginValidation(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @validates("email")
    def validate_email(self, value):
        if not User.email_exist(email=value):
            raise ValidationError("Email does not exist")


class NewPasswordValidation(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=8))
    password2 = fields.Str(required=True, validate=validate.Length(min=8))

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data['password'] != data['password2']:
            raise ValidationError("Password does not match")


class UserUpdateValidation(Schema):
    email = fields.Email(required=False, validate=validate.Length(min=3))
    username = fields.Str(required=False, validate=validate.Length(min=3))
    active = fields.Bool(required=False)
    superadmin = fields.Bool(required=False)
