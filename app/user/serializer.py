from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,auto_field
from .models import User

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ('id','username','email','active')