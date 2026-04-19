"""
routes/auth.py — Authentication Routes (Register, Login, Logout)

WHAT IS AUTHENTICATION?
Authentication answers the question: "WHO are you?"
It's the process of proving your identity (usually with a username + password).

WHAT IS A SESSION?
After logging in, we need to REMEMBER that the user is logged in
for their next request. We use a SESSION — a small piece of encrypted
data stored in a cookie in the user's browser.

Think of it like a wristband at a concert: you prove your identity once
(at the gate), get a wristband, and then you can walk around freely.
"""

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
import sqlite3

# A Blueprint is like a "sub-application" — it groups related routes together
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Create a new user account.

    Expects JSON: {"username": "alice", "email": "alice@mail.com", "password": "secret123"}
    """
    data = request.get_json()
    #   request.get_json() reads the JSON body sent by the frontend

    # --- INPUT VALIDATION ---
    # NEVER trust data from the client! Always validate it.
    # A user (or attacker) could send anything — empty strings, missing fields, etc.
    if not data:
        return jsonify({"error": "No data provided"}), 400
        #   400 = "Bad Request" — the client sent something wrong

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    # --- PASSWORD HASHING ---
    # NEVER store passwords in plain text!
    # If your database is ever hacked, attackers would have everyone's password.
    #
    # Instead, we store a HASH — a one-way scrambled version.
    # "secret123" becomes something like "pbkdf2:sha256:260000$abc123..."
    # You CANNOT reverse a hash back to the original password.
    #
    # When the user logs in, we hash their input and COMPARE the hashes.
    password_hash = generate_password_hash(password)

    # --- INSERT INTO DATABASE ---
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        db.commit()
    except sqlite3.IntegrityError:
    # UNIQUE constraint violated → real "already exists" case
        return jsonify({"error": "Username or email already exists"}), 409
    except sqlite3.OperationalError as e:
    # Schema mismatch, missing column, etc. — surface it
        return jsonify({"error": f"Database error: {e}"}), 500

    return jsonify({"message": "Account created successfully!"}), 201
    #   201 = "Created" — a new resource was successfully created


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Log in to an existing account.

    Expects JSON: {"username": "alice", "password": "secret123"}
    """
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    # Look up the user in the database
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username = ?",
        (data['username'],)
    ).fetchone()

    # Check if user exists AND password is correct
    if user is None or not check_password_hash(user['password_hash'], data['password']):
        return jsonify({"error": "Invalid username or password"}), 401
        #   We give a VAGUE error on purpose!
        #   We don't say "user not found" or "wrong password" separately
        #   because that would help attackers figure out which usernames exist.

    # --- CREATE SESSION ---
    # Store the user's ID in the session cookie
    session['user_id'] = user['id']
    session['username'] = user['username']

    return jsonify({
        "message": "Logged in successfully",
        "user": {
            "id": user['id'],
            "username": user['username'],
            "email": user['email']
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Log out — clear the session."""
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Check if the user is currently logged in, and return their info."""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    db = get_db()
    user = db.execute("SELECT id, username, email FROM users WHERE id = ?",
                      (session['user_id'],)).fetchone()

    if not user:
        session.clear()
        return jsonify({"error": "User not found"}), 401

    return jsonify(dict(user)), 200