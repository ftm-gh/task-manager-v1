"""
middleware/auth.py — Authentication Middleware

WHAT IS MIDDLEWARE?
Middleware is code that runs BETWEEN receiving a request and processing it.
Think of it as a security guard at the door of a building:
before you can enter any room (route), the guard checks your badge (session).

WHAT IS A DECORATOR?
In Python, a decorator is a function that WRAPS another function to add
extra behavior. The @login_required decorator adds an authentication check
before any route that uses it.

Without decorators, you'd have to copy-paste the auth check into EVERY route.
That violates DRY (Don't Repeat Yourself).
"""

from functools import wraps
from flask import session, jsonify


def login_required(f):
    """
    A decorator that checks if the user is logged in before
    allowing access to a route.

    Usage:
        @tasks_bp.route('/api/tasks')
        @login_required              ← just add this line!
        def get_tasks():
            ...

    If the user is NOT logged in, they get a 401 Unauthorized response.
    If the user IS logged in, the route runs normally.
    """

    @wraps(f)
    # @wraps preserves the original function's name and docstring.
    # Without it, every decorated function would be named "decorated_function"
    # which makes debugging confusing.
    def decorated_function(*args, **kwargs):
        # 'session' is Flask's built-in way to track logged-in users.
        # It stores data in an encrypted cookie in the user's browser.
        # When a user logs in, we store their user_id in the session.
        if 'user_id' not in session:
            return jsonify({
                "error": "Authentication required. Please log in."
            }), 401
            #   401 = "Unauthorized" HTTP status code
            #   This tells the frontend: "This user isn't logged in"

        # If we get here, the user IS logged in — proceed to the actual route
        return f(*args, **kwargs)

    return decorated_function