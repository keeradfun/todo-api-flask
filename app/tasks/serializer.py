from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Tasks


class TaskSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = Tasks
        load_instance = True
        fields = ('id', 'title', 'description',
                  'deadline', 'status', 'created_at', 'updated_at')
