from .models import User
from marshmallow import Schema, fields, validate, ValidationError,validates
from flask_marshmallow import Marshmallow

class RegisterSchema(Schema):
    email = fields.Email(required=True,validate=validate.Length(min=3))
    username = fields.Str(required=True,validate=validate.Length(min=3))
    password = fields.Str(required=True,validate=validate.Length(min=8))
    @validates("email")
    def validate_email(self,value):
        if User.email_exist(email = value):
            raise ValidationError("Email already taken")
        
    @validates("username")
    def validate_username(self,value):
        if User.username_exist(username = value):
            raise ValidationError("Username already taken")


class LoginSchema(Schema):
    email = fields.Email(required=True,validate=validate.Length(min=3))
    password = fields.Str(required=True,validate=validate.Length(min=8))
    @validates("email")
    def validate_email(self,value):
        if not User.email_exist(email = value):
            raise ValidationError("Email does not exist")
