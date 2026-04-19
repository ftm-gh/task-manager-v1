"""
app.py — Application Entry Point

This is where our Flask application is CREATED and CONFIGURED.

We use a pattern called the APPLICATION FACTORY:
instead of creating the app at the top level, we put it inside
a function called create_app(). Why?
  1. We can create different versions (testing vs. production)
  2. We can create multiple instances if needed
  3. It keeps things clean and organized
"""

from flask import Flask
from flask_cors import CORS
from database import init_db
from config import Config, TestConfig


def create_app(testing=False):
    """
    Create and configure the Flask application.

    Parameters:
        testing: If True, use test configuration (separate database, etc.)
    """

    # Create the Flask app
    # __name__ tells Flask where to find files relative to this module
    app = Flask(__name__)

    # Load configuration
    if testing:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    # Enable CORS (Cross-Origin Resource Sharing)
    # WHAT IS CORS?
    # Your frontend runs on http://localhost:5173
    # Your backend runs on http://localhost:5000
    # Browsers BLOCK requests between different origins (ports) by default.
    # This is a SECURITY feature called the Same-Origin Policy.
    # CORS tells the browser: "It's OK, I trust requests from this other origin."
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    # Initialize the database (create tables if they don't exist)
    init_db(app.config.get('DATABASE'))

    # REGISTER BLUEPRINTS
    # Blueprints are Flask's way of organizing routes into separate files.
    # Without blueprints, ALL routes would be in this one file — messy!
    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    from routes.categories import categories_bp

    app.register_blueprint(auth_bp)        # adds /api/auth/...  routes
    app.register_blueprint(tasks_bp)       # adds /api/tasks/...  routes
    app.register_blueprint(categories_bp)  # adds /api/categories/... routes

    return app


# This block runs ONLY when you execute "python app.py" directly
# It does NOT run when this file is imported by another file (like tests)
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
    #   debug=True: auto-restarts when you change code, shows detailed errors
    #   port=5000: the app listens on http://localhost:5000