from flask import jsonify
from ..models import MyTask, db
from werkzeug.security import generate_password_hash, check_password_hash


def get_all_tasks():
    tasks = MyTask.query.order_by(MyTask.created).all()
    return jsonify([{
        'id': task.id,
        'content': task.content,
        'complete': task.complete,
        'created': task.created.isoformat()
    } for task in tasks])

def create_task(data):
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

def get_task_by_id(task_id):
    task = MyTask.query.get_or_404(task_id)
    return jsonify({
        'id': task.id,
        'content': task.content,
        'complete': task.complete,
        'created': task.created.isoformat()
    })

def update_task(task_id, data):
    task = MyTask.query.get_or_404(task_id)
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

def delete_task(task_id):
    task = MyTask.query.get_or_404(task_id)
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
