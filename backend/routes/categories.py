"""
   routes/categories.py — Category API Endpoints

This file defines the API endpoints (URLs) for managing categories.

🔑 KEY CONCEPT: What is a Blueprint?

A Blueprint is Flask's way of organizing routes into separate files.
Without blueprints, ALL routes would be in one giant app.py file.

With blueprints, you can split routes into logical groups:
- routes/auth.py      → /api/register, /api/login
- routes/tasks.py     → /api/tasks, /api/tasks/<id>
- routes/categories.py → /api/categories, /api/categories/<id>

Each blueprint is like a "mini-app" that gets registered with the main app.

Think of it like departments in a company:
- HR department handles hiring/firing
- Sales department handles customers
- Each department has its own rules, but they're all part of one company.


🔑 KEY CONCEPT: RESTful API Design

REST is a convention for how URLs and HTTP methods should be organized:

HTTP Method | URL                    | Action
----------- | ---------------------- | ----------------
GET         | /api/categories        | List all categories
POST        | /api/categories        | Create a new category
GET         | /api/categories/5      | Get category #5
PUT         | /api/categories/5      | Update category #5
DELETE      | /api/categories/5      | Delete category #5

Notice:
- The SAME URL can do different things based on the HTTP method
- GET = read, POST = create, PUT = update, DELETE = remove
- This is clean and predictable
  """

from flask import Blueprint, request, jsonify, session
"""
Blueprint: for organizing routes (explained above)
request: contains data sent by the client (JSON body, headers, etc.)
jsonify: converts a Python dict to a JSON response
"""

from models.category import Category
from middleware.auth import login_required
"""
login_required is a DECORATOR that:
1. Checks if the request has a valid JWT token
2. If yes → allows the request, and passes the current user
3. If no → returns a 401 Unauthorized error

We import it from auth.py so we don't have to rewrite the logic.
"""

# Create a Blueprint named 'categories'
categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')
"""
'categories' → the name of this blueprint (used internally by Flask)
__name__ → tells Flask where to find this module (Python magic variable)
"""


@categories_bp.route('', methods=['GET'])
@login_required
def get_categories():
    """
    GET /api/categories

    Returns all categories belonging to the logged-in user.
    
    🔑 How the decorators work (reading bottom to top):
    
    1. @login_required runs FIRST:
       - Checks the JWT token in the Authorization header
       - If invalid, returns 401 error (this function never runs)
    
    2. @categories_bp.route(...) registers this function for GET /api/categories
    
    It's the User object of whoever is making the request.
    """
    categories = Category.get_all_by_user(session['user_id'])
    # Get all categories for this specific user

    return jsonify({
        'categories': [cat.to_dict() for cat in categories]
    })
    """
    Convert each Category object to a dictionary, then return as JSON.
    
    Response looks like:
    {
        "categories": [
            {"id": 1, "name": "Work", "color": "#e74c3c", "user_id": 1},
            {"id": 2, "name": "Personal", "color": "#3498db", "user_id": 1}
        ]
    }
    """


@categories_bp.route('', methods=['POST'])
@login_required
def create_category():
    """
    POST /api/categories

    Create a new category.
    
    Expected JSON body:
    {
        "name": "Work",
        "color": "#e74c3c"   ← optional, defaults to blue
    }
    """
    data = request.get_json() or {}
    """
    request.get_json() reads the JSON body sent by the frontend.
    
    When the frontend does:
        api.post('/api/categories', { name: 'Work', color: '#e74c3c' })
    
    That data arrives here as a Python dictionary:
        data = {"name": "Work", "color": "#e74c3c"}
    """

    # ── Validation ──
    if not data or not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400
        """
        Return a 400 Bad Request error.
        
        The second value (400) is the HTTP status code.
        Common status codes:
          200 = OK (success)
          201 = Created (something new was made)
          400 = Bad Request (client sent invalid data)
          401 = Unauthorized (not logged in)
          404 = Not Found
          500 = Internal Server Error (server crashed)
        
        data.get('name') is safer than data['name'] because:
        - data['name'] CRASHES if 'name' doesn't exist (KeyError)
        - data.get('name') returns None if 'name' doesn't exist
        """

    name = data['name'].strip()
    """
    .strip() removes whitespace from both ends (like .trim() in JavaScript).
    "  Work  ".strip() → "Work"
    """

    if len(name) == 0:
        return jsonify({'error': 'Category name cannot be empty'}), 400

    color = data.get('color', '#3498db')
    """
    .get(key, default) returns the value for key, or default if key doesn't exist.
    
    If the frontend sent a color → use it.
    If not → use '#3498db' (blue).
    """

    category = Category.create(name, session['user_id'], color)

    return jsonify({
        'message': 'Category created successfully',
        'category': category.to_dict()
    }), 201
    # 201 Created — tells the client something was successfully created


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    """
    PUT /api/categories/5

    Update an existing category.
    
    🔑 What is <int:category_id>?
    
    This is a URL PARAMETER (also called a "route parameter" or "path variable").
    <int:category_id> means:
    - Extract a value from the URL
    - Convert it to an integer (int)
    - Pass it to the function as the "category_id" parameter
    
    URL: /api/categories/5  → category_id = 5
    URL: /api/categories/12 → category_id = 12
    
    If someone sends /api/categories/abc, Flask returns 404
    because "abc" can't be converted to int.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Only include fields that were actually sent
    name = data.get('name')
    color = data.get('color')

    if name is not None:
        name = name.strip()
        if len(name) == 0:
            return jsonify({'error': 'Category name cannot be empty'}), 400

    category = Category.update(category_id, session['user_id'], name=name, color=color)

    if not category:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({
        'message': 'Category updated successfully',
        'category': category.to_dict()
    })


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    """
    DELETE /api/categories/5

    Delete a category. Tasks in this category become uncategorized (not deleted).
    """
    success = Category.delete(category_id, session['user_id'])

    if not success:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({'message': 'Category deleted successfully'})
    # Default status code is 200 (OK)