from .models import Tasks
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from .validation import TasksValidationSchema, TaskUpdateValidationSchema
from marshmallow import ValidationError
from flask import request
from .serializer import TasksSchema


class TaskCreate(Resource):
    @jwt_required()
    def post(self):
        try:
            json_data = request.get_json(force=True)
            validated_data = TasksValidationSchema().load(data=json_data)
            if validated_data:
                new_task = Tasks.create_task(
                    description=validated_data['description'],
                    title=validated_data['title'],
                    deadline=validated_data['deadline']
                )
                if new_task:
                    return {
                        "status": 200,
                        "message": "task created successfully",
                        "Code": "OK"
                    }
                else:
                    return {
                        "status": 400,
                        "message": "failed to create task",
                        "code": "BAD_REQUEST"
                    }, 400
        except ValidationError as err:
            return {
                "status": 400,
                "message": err.messages,
                "code": "BAD_REQUEST"
            }, 400
        return {
            "status": "success"
        }


class TaskFindById(Resource):
    @jwt_required()
    def get(self, id):
        if current_user:
            task = Tasks.get_task_by_id(id=id, user_id=current_user.id)
            if task:
                serialized_task = TasksSchema().dump(task)
                return {
                    "status": 200,
                    "data": {
                        "task": serialized_task
                    },
                    "code": "OK"
                }, 200
            else:
                return {
                    "status": 400,
                    "message": "Invalid user id",
                    "code": "BAD_REQUEST"
                }, 400
        else:
            return {
                "status": 403,
                "error": "Not Found",
                "message": "You are not allowed to access resource",
                "code": "UNAUTHORIZED"
            }


class TaskByDate(Resource):
    @jwt_required
    def get(self, date):
        if current_user:
            task = Tasks.get_tasks_by_date(
                deadline=date, user_id=current_user.id)
            if task:
                serialized_task = TasksSchema().dump(task)
                return {
                    "status": 200,
                    "data": {
                        "task": serialized_task
                    },
                    "code": "OK"
                }, 200
            else:
                return {
                    "status": 400,
                    "message": "Invalid user id",
                    "code": "BAD_REQUEST"
                }, 400
        else:
            return {
                "status": 403,
                "error": "Not Found",
                "message": "You are not allowed to access resource",
                "code": "UNAUTHORIZED"
            }


class AllTasks(Resource):
    @jwt_required
    def get(self):
        if current_user:
            tasks = Tasks.get_all_tasks(user_id=current_user.id)
            if tasks:
                serialized_task = TasksSchema().dump(tasks)
                return {
                    "status": 200,
                    "data": {
                        "tasks": serialized_task
                    },
                    "code": "OK"
                }, 200
            else:
                return {
                    "status": 400,
                    "message": "Invalid user id",
                    "code": "BAD_REQUEST"
                }, 400
        else:
            return {
                "status": 403,
                "error": "Not Found",
                "message": "You are not allowed to access resource",
                "code": "UNAUTHORIZED"
            }


class DeleteTask(Resource):
    @jwt_required
    def delete(self, id):
        if current_user:
            task = Tasks.delete_task(user_id=current_user.id)
            if task:
                return {
                    "status": "200",
                    "message": "Successfully deleted the task",
                    "code": "OK"
                }
            else:
                return {
                    "status": 400,
                    "message": "Invalid task id",
                    "code": "BAD_REQUEST"
                }, 400
        else:
            return {
                "status": 403,
                "error": "Not Found",
                "message": "You are not allowed to access resource",
                "code": "UNAUTHORIZED"
            }


class UpdateTask(Resource):
    @jwt_required
    def post(self, id):
        json_data = request.get_json(force=True)
        validated_data = TasksValidationSchema().load(data=json_data)
        if validated_data:
            update = Tasks.update_task(id, validated_data)
            if update:
                return {
                    "status": 200,
                    "message": "task updated successfully",
                    "Code": "OK"
                }
            else:
                return {
                    "status": 400,
                    "message": "Failed to update task",
                    "code": "BAD_REQUEST"
                }, 400