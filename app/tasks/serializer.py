from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from .models import Tasks


class TasksSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tasks
        load_instance = True
        fields = ('id', 'title', 'description',
                  'deadline', 'status', 'created_at', 'updated_at')
