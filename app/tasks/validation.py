from .models import Tasks
from marshmallow import Schema, fields, validate, ValidationError, validates, validates_schema


class TasksValidationSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str(required=True, validate=validate.Length(min=3))
    deadline = fields.DateTime(required=True)


class TaskUpdateValidationSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=3))
    description = fields.Str(required=False, validate=validate.Length(min=3))
    deadline = fields.DateTime(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(
        ['PENDING', 'ONGOING', 'COMPLETED']))
