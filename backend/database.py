"""
database.py — Database Connection Helper

This module handles connecting to SQLite and initializing the schema.

PRINCIPLE: Don't Repeat Yourself (DRY)
Instead of writing database connection code in every file that needs it,
we write it ONCE here, and import it everywhere else.
"""

import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'tasks.db')


def get_db(db_path=None):
    """
    Open a connection to the SQLite database.

    Returns a connection object that you can use to execute SQL.

    Parameters:
        db_path: Optional path to the database file.
                 If not provided, uses the default path.
    """
    path = db_path or DATABASE
    conn = sqlite3.connect(path)

    # By default, sqlite3 returns rows as tuples: (1, 'alice', 'alice@mail.com')
    # Row factory lets us access columns by NAME: row['username']
    # This makes our code much more readable!
    conn.row_factory = sqlite3.Row

    # SQLite has foreign keys but they're DISABLED by default (for backward compatibility).
    # We must explicitly turn them on for every connection.
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def close_db(conn):
    """Close the database connection."""
    if conn is not None:
        conn.close()


def init_db(db_path=None):
    """
    Create all tables defined in schema.sql.

    This is called once when the app starts for the first time,
    or when running tests (to create a fresh database).
    """
    conn = get_db(db_path)
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
        #   executescript() runs multiple SQL statements at once
        #   It reads our entire schema.sql and creates all tables

    conn.commit()
    conn.close()
    print("Database initialized successfully!")