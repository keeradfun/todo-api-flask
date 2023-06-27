from app.database import db
from sqlalchemy.sql import func
from sqlalchemy import exc
from sqlalchemy import delete


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

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return "Something went wrong"

    @classmethod
    def findone(cls, id, user_id):
        try:
            task = cls.query.filter_by(id=id, user=user_id).first()
            if (task):
                return task
            else:
                return None
        except:
            return None

    @classmethod
    def findall(cls, user_id):
        try:
            tasks = Tasks.query.filter_by(user=user_id).all()
            if (tasks):
                return tasks
            else:
                return None
        except:
            return None

    @classmethod
    def update(cls, id, user_id, data):
        try:
            task = Tasks.query.filter_by(id=id, user=user_id).update(
                data, synchronize_session=False)
            db.session.commit()
            return task
        except:
            return task

    @classmethod
    def delete(cls, id, user_id):
        try:
            Tasks.query.filter_by(id=id, user=user_id).delete()
            db.session.commit()
            return True
        except:
            return None

    @classmethod
    def filter_task(cls, data):
        args = cls._filter_generator(data)
        tasks = cls.query.filter(*args)
        print(tasks)
        if tasks:
            return tasks
        else:
            return None

    @classmethod
    def _filter_generator(cls, data):
        args = []
        contains_fields = ['title', 'description']
        exact_fields = ['deadline', 'status']

        for key, value in data.items():
            if key in exact_fields:
                args.append(getattr(cls, key) == data[key])

            if key in contains_fields:
                args.append(getattr(cls, key).contains(data[key]))
        return args
