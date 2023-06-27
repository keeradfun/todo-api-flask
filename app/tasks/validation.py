from marshmallow import Schema, fields, validate


class TasksCreateValidation(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str(required=True, validate=validate.Length(min=3))
    deadline = fields.DateTime(required=True)


class TaskUpdateValidation(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=3))
    description = fields.Str(required=False, validate=validate.Length(min=3))
    deadline = fields.DateTime(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(
        ['PENDING', 'ONGOING', 'COMPLETED']))


class TaskFilterValidation(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=3))
    description = fields.Str(required=False, validate=validate.Length(min=3))
    deadline = fields.DateTime(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(
        ['PENDING', 'ONGOING', 'COMPLETED']))
