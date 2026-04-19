"""
routes/tasks.py — Task CRUD API

This is the HEART of our application. Each function handles one
type of HTTP request for tasks.

PRINCIPLE: Each route function should be SHORT and READABLE.
It should:
  1. Read input from the request
  2. Validate the input
  3. Call the model to do the database work
  4. Return a response

The route does NOT contain SQL — that's the model's job.
The route does NOT contain HTML — that's the frontend's job.
"""

from flask import Blueprint, request, jsonify, session
from models.task import TaskModel
from middleware.auth import login_required

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@tasks_bp.route('', methods=['POST'])
@login_required
def create_task():
    """
    Create a new task.

    HTTP: POST /api/tasks
    Body: {"title": "Buy milk", "priority": "high", "due_date": "2026-04-10"}
    Response: 201 Created + the new task as JSON
    """
    data = request.get_json()

    if not data or not data.get('title', '').strip():
        return jsonify({"error": "Title is required"}), 400

    task = TaskModel.create(
        title=data['title'].strip(),
        description=data.get('description', '').strip(),
        priority=data.get('priority', 'medium'),
        due_date=data.get('due_date'),
        category_id=data.get('category_id'),
        user_id=session['user_id']
        #   session['user_id'] was set when the user logged in.
        #   This ensures the task is linked to the correct user.
    )
    return jsonify(task), 201


@tasks_bp.route('', methods=['GET'])
@login_required
def get_tasks():
    """
    Get all tasks for the current user, with optional filters.

    HTTP: GET /api/tasks
          GET /api/tasks?completed=1
          GET /api/tasks?priority=high
          GET /api/tasks?category_id=3
    Response: 200 OK + array of tasks as JSON
    """
    # request.args contains URL query parameters (?key=value)
    filters = {
        "is_completed": request.args.get('completed'),
        "priority": request.args.get('priority'),
        "category_id": request.args.get('category_id'),
    }

    tasks = TaskModel.get_all(user_id=session['user_id'], filters=filters)
    return jsonify(tasks), 200


@tasks_bp.route('/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    """
    Get a single task by ID.

    HTTP: GET /api/tasks/5
    The <int:task_id> in the route means Flask will:
      - Extract "5" from the URL
      - Convert it to an integer
      - Pass it as the task_id parameter
    """
    task = TaskModel.get_by_id(task_id, user_id=session['user_id'])
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """
    Update an existing task.

    HTTP: PUT /api/tasks/5
    Body: {"title": "Updated title", "is_completed": 1}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    task = TaskModel.update(task_id, user_id=session['user_id'], data=data)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """
    Delete a task.

    HTTP: DELETE /api/tasks/5
    """
    success = TaskModel.delete(task_id, user_id=session['user_id'])
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 200