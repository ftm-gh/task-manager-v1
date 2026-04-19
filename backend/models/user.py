"""
   models/user.py — User Model

🔑 KEY CONCEPT: What is a Model?

A model is a Python class that represents a DATABASE TABLE.
It provides methods to interact with the table:
- Create a new user (INSERT)
- Find a user by username (SELECT)
- Verify a password

Instead of writing raw SQL everywhere in your code, you write it
in ONE place (the model) and call clean methods from your routes.

This is part of a pattern called "Separation of Concerns":
- Routes handle HTTP requests/responses
- Models handle database operations
- Each file has ONE job

Think of it like a restaurant:
- The waiter (route) takes your order
- The chef (model) prepares the food
- The waiter doesn't cook, the chef doesn't serve
  """

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
"""
What is werkzeug?
Werkzeug is a library that Flask is built on top of.
It provides useful utilities, including password hashing functions.

generate_password_hash("secret123") → "$pbkdf2:sha256:260000$..."
Takes a plain password and returns a hashed (encrypted) version.

check_password_hash(hash, "secret123") → True or False
Checks if a plain password matches a stored hash.
This is how we verify passwords during login WITHOUT ever
storing the actual password.
"""

from database import get_db


class User:
    """
    The User model — handles all database operations for users.

    🔑 KEY CONCEPT: What is a Class?
    
    A class is a BLUEPRINT for creating objects.
    Think of it like a cookie cutter:
    - The class (cookie cutter) defines the shape
    - Each object (cookie) is created from that shape
    
    class User:
        - Defines what a user IS (id, username, password_hash)
        - Defines what a user can DO (create, find, check_password)
    
    user1 = User(1, "alice", "hash...")  ← one specific user
    user2 = User(2, "bob", "hash...")    ← another specific user
    Both are User objects, but with different data.
    """

    def __init__(self, id, username, email, password_hash):
        """
        __init__ is the CONSTRUCTOR — it runs when you create a new User object.
        
        "self" refers to the specific object being created.
        It's like "this" in JavaScript or Java.
        
        self.id = id means:
        "Store the id parameter as a property of THIS user object."
        
        After: user = User(1, "alice", "hash...")
        You can do: user.id → 1, user.username → "alice"
        """
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def create(username, email, password):
        """
        Create a new user in the database.
        
        🔑 What is @staticmethod?
        A static method belongs to the CLASS, not to a specific object.
        You call it as: User.create("alice", "secret")
        NOT as: some_user.create("alice", "secret")
        
        It doesn't receive "self" because there's no specific user object involved.
        We're CREATING a new user, so no user exists yet.
        
        Returns: a User object if successful
        Raises: an exception if the username already exists
        """
        db = get_db()

        password_hash = generate_password_hash(password)
        # Convert plain password to a secure hash

        try:
            cursor = db.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            """
            🔑 KEY CONCEPT: Parameterized Queries (the ? placeholders)
            
            NEVER do this (string concatenation):
                f"INSERT INTO users VALUES ('{username}', '{password_hash}')"
            
            Why? SQL Injection attack!
            If someone enters username: alice'; DROP TABLE users; --
            The query becomes:
                INSERT INTO users VALUES ('alice'; DROP TABLE users; --', '...')
            This DELETES YOUR ENTIRE TABLE!
            
            Instead, use ? placeholders:
                'INSERT INTO users (username, password_hash) VALUES (?, ?)'
                (username, password_hash)
            
            The database treats the values as DATA, not as SQL commands.
            Even if someone enters malicious text, it's stored as plain text.
            
            This is called a PARAMETERIZED QUERY and is the #1 defense
            against SQL injection — one of the most common web attacks.
            
            
            What is a cursor?
            A cursor is an object that lets you interact with query results.
            After an INSERT, cursor.lastrowid gives you the new row's ID.
            """

            db.commit()
            """
            🔑 What is commit()?
            
            Database changes are NOT saved automatically.
            They exist in a "transaction" — a temporary staging area.
            
            commit() SAVES (persists) the changes permanently.
            If your program crashes before commit(), the changes are LOST.
            This is actually a SAFETY feature — if something goes wrong halfway
            through multiple operations, nothing is saved (all or nothing).
            
            This is called "ACID transactions" — a core database concept.
            """

            return User(cursor.lastrowid, username, email, password_hash)
            # Return a User object with the auto-generated ID

        except sqlite3.IntegrityError:
            """
            IntegrityError is raised when a database CONSTRAINT is violated.
            In our case: the UNIQUE constraint on username.
            If someone tries to register "alice" and "alice" already exists,
            SQLite raises IntegrityError.
            """
            raise ValueError('Username already exists')
            # We convert it to a ValueError with a friendly message
            # The route will catch this and return an error to the user

    @staticmethod
    def find_by_username(username):
        """
        Look up a user by their username.
        
        Returns: a User object if found, None if not found.
        
        Used during login: find the user, then check their password.
        """
        db = get_db()

        row = db.execute('SELECT * FROM users WHERE username = ?',(username,)).fetchone()
        """
        Note the comma after username: (username,)
        
        In Python, (username) is just parentheses (grouping).
        (username,) is a TUPLE with one element.
        
        The execute() method expects a tuple (or list) for the parameters.
        Without the comma, Python would pass a string, not a tuple,
        and you'd get a confusing error.
        
        This is a common Python gotcha that trips up beginners!
        """
        """
        .fetchone() retrieves ONE row from the result.
        - If a matching row exists → returns the row (a dict-like object)
        - If no match → returns None
        
        Other options:
        .fetchall() → returns ALL matching rows as a list
        .fetchmany(5) → returns up to 5 rows
        """

        if row:
            return User(row['id'], row['username'], row['email'], row['password_hash'])
            # Create and return a User object from the database row
        return None
        # No user found with that username

    @staticmethod
    def find_by_id(user_id):
        """
        Look up a user by their ID.
        Used to get user info from the JWT token (which contains the user ID).
        """
        db = get_db()

        row = db.execute(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()

        if row:
            return User(row['id'], row['username'], row['email'], row['password_hash'])
        return None

    def check_password(self, password):
        """
        Verify a password against this user's stored hash.
        
        This is an INSTANCE method (not static) — it operates on a specific user.
        "self" is the user whose password we're checking.
        
        Returns: True if password is correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
        # werkzeug handles the comparison securely

    def to_dict(self):
        """
        Convert the User object to a dictionary.
        
        🔑 Why?
        When we send data back to the frontend (as JSON), we need a dictionary.
        Python objects can't be directly converted to JSON.
        
        Also: we EXCLUDE password_hash! Never send password data to the client.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
            # Notice: NO password_hash here — security!
        }