from flask import request, jsonify
from . import db
from .models import MyTask
from .controllers import task_controller


def init_routes(app):
    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        return task_controller.get_all_tasks()

    @app.route("/tasks", methods=["POST"])
    def add_task():
        data = request.get_json()
        return task_controller.create_task(data)

    @app.route("/tasks/<int:id>", methods=["GET"])
    def get_task(id: int):
        return task_controller.get_task_by_id(id)

    @app.route("/tasks/<int:id>", methods=["PUT"])
    def update_task(id: int):
        data = request.get_json()
        return task_controller.update_task(id, data)

    @app.route("/tasks/<int:id>", methods=["DELETE"])
    def delete_task(id: int):
        return task_controller.delete_task(id)
