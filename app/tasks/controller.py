from flask import request, abort
from .models import Tasks
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from .validation import TasksCreateValidation, TaskFilterValidation, TaskUpdateValidation
from marshmallow import ValidationError
from .serializer import TaskSerializer


class TasksManager(Resource):
    @jwt_required()
    def post(self):
        try:
            json_data = request.get_json(force=True)
            validated_data = TasksCreateValidation().load(data=json_data)
            if validated_data:
                new_task = Tasks(
                    user=current_user.id,
                    title=validated_data['title'],
                    description=validated_data['description'],
                    deadline=validated_data['deadline'],
                    status="PENDING"
                )
                new_task.create()
                if new_task:
                    return {
                        "status": True,
                        "task": TaskSerializer().dump(new_task)
                    }, 200
                else:
                    return {
                        "status": False,
                        "message": "failed to create task"
                    }, 400
        except ValidationError as err:
            return {
                "status": False,
                "message": err.messages
            }, 400

    @jwt_required()
    def get(self):
        try:
            tasks = Tasks.findall(user_id=current_user.id)
            if tasks:
                serialized_data = []
                for task in tasks:
                    serialized_data.append(TaskSerializer().dump(task))

                return {
                    "status": True,
                    "tasks": serialized_data
                }, 200
        except Exception as e:
            abort(422)


class Filter(Resource):
    @jwt_required()
    def post(self):
        try:
            json_data = request.get_json(force=True)
            validated_data = TaskFilterValidation().load(data=json_data)
            if validated_data:
                tasks = Tasks.filter_task(validated_data)
                if tasks:
                    serialized_task = []
                    for task in tasks:
                        serialized_task.append(TaskSerializer().dump(task))
                    return {
                        "status": True,
                        "tasks": serialized_task,
                    }, 200
                else:
                    return {
                        "status": False,
                        "message": "No tasks found"
                    }, 400

        except ValidationError as err:
            return {
                "status": False,
                "message": err.messages
            }, 400


class TaskManager(Resource):
    @jwt_required()
    def get(self, id):
        try:
            task = Tasks.findone(id=id, user_id=current_user.id)
            if task:
                serialized_task = TaskSerializer().dump(task)
                return {
                    "status": True,
                    "user": serialized_task
                }
            else:
                return {
                    "status": False,
                    "message": "user not found"
                }, 400
        except:
            abort(422)

    @jwt_required()
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            if json_data:
                validated_data = TaskUpdateValidation().load(data=json_data)
                if validated_data:
                    task = Tasks.update(id, current_user.id, validated_data)
                    if task:
                        task = Tasks.findone(id=id, user_id=current_user.id)
                        return {
                            "status": True,
                            "user": TaskSerializer().dump(task)
                        }, 200
                    else:
                        return {
                            "status": False,
                            "message": "Invalid user id"
                        }, 400

        except ValidationError as err:
            return {
                "status": False,
                "message": err.messages
            }, 400

    @jwt_required()
    def delete(self, id):
        try:
            task = Tasks.delete(id=id, user_id=current_user.id)
            if task:
                return {
                    "status": True,
                    "message": "success"
                }, 200
            else:
                return {
                    "status": False,
                    "message": "Can not delete"
                }, 400
        except:
            abort(422)
