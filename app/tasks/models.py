from app.database import db
from sqlalchemy.sql import func
from sqlalchemy import exc


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @staticmethod
    def create_task(title: str, description: str, deadline, user):
        try:
            new_task = Tasks(
                user=user.id,
                title=title,
                description=description,
                deadline=deadline,
                status="PENDING"
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task
        except exc.SQLAlchemyError:
            return "Something went wrong"

    def get_task_by_id(id, user_id):
        try:
            task = Tasks.query.filter_by(id=id, user=user_id).first()
            if (task):
                return task
            else:
                return None
        except:
            return None

    def get_all_tasks(user_id):
        try:
            tasks = Tasks.query.filter_by(user=user_id).all()
            if (tasks):
                return tasks
            else:
                return None
        except:
            return None

    def delete_task(id, user_id):
        try:
            task = Tasks.query.filter_by(
                id=id, user__id=user_id).first().delete()
            db.session.delete(task)
            return True
        except:
            return None

    def update_task(id, data):
        try:
            task = Tasks.query.filter(id=id).update(
                data, synchronize_session=False)
            db.session.commit()
            return True
        except:
            return None
