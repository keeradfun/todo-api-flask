from app.database import db
from sqlalchemy.sql import func


class Tasks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer,db.ForeignKey("user.id"))
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(250),nullable=False)
    deadline = db.Column(db.DateTime(),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())