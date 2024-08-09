from flask import request, jsonify
from . import db
from .models import MyTask


def init_routes(app):
    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        tasks = MyTask.query.order_by(MyTask.created).all()
        return jsonify([{
            'id': task.id,
            'content': task.content,
            'complete': task.complete,
            'created': task.created.isoformat()
        } for task in tasks])

    @app.route("/tasks", methods=["POST"])
    def add_task():
        data = request.get_json()
        content = data.get('content')
        if not content:
            return jsonify({"error": "Content is required"}), 400
        new_task = MyTask(content=content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return jsonify({
                'id': new_task.id,
                'content': new_task.content,
                'complete': new_task.complete,
                'created': new_task.created.isoformat()
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/tasks/<int:id>", methods=["GET"])
    def get_task(id: int):
        task = MyTask.query.get_or_404(id)
        return jsonify({
            'id': task.id,
            'content': task.content,
            'complete': task.complete,
            'created': task.created.isoformat()
        })

    @app.route("/tasks/<int:id>", methods=["PUT"])
    def update_task(id: int):
        data = request.get_json()
        task = MyTask.query.get_or_404(id)
        content = data.get('content')
        complete = data.get('complete')

        if content:
            task.content = content
        if complete is not None:
            task.complete = complete

        try:
            db.session.commit()
            return jsonify({
                'id': task.id,
                'content': task.content,
                'complete': task.complete,
                'created': task.created.isoformat()
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/tasks/<int:id>", methods=["DELETE"])
    def delete_task(id: int):
        task = MyTask.query.get_or_404(id)
        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Task deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
