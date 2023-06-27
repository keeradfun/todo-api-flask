from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import User


class UserSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ('id', 'username', 'email', 'active', 'superadmin')
