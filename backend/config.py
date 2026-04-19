import os

# os.path.dirname(__file__) gives us the folder this file lives in
# This ensures the database file is created next to our code
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Base configuration — shared by all environments."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    #   SECRET_KEY is used by Flask to encrypt session cookies.
    #   os.environ.get() tries to read it from an ENVIRONMENT VARIABLE first.
    #   If it's not set (during development), it falls back to a default.
    #   In production, you MUST set a real random secret!

    DATABASE = os.path.join(BASE_DIR, 'tasks.db')
    #   Path to our SQLite database file


class TestConfig(Config):
    """Configuration for automated tests."""

    TESTING = True
    DATABASE = os.path.join(BASE_DIR, 'test_tasks.db')
    #   Tests use a SEPARATE database so they don't mess up real data
    