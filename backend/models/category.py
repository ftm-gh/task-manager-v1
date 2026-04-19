"""
   models/category.py — Category Model

Categories let users organize their tasks (e.g., "Work", "Personal", "Shopping").
Each category has a name and a color for visual distinction.

This model follows the same pattern as User:
- Static methods for database operations
- Instance methods for object-level operations
  """

import sqlite3
from database import get_db
# We reuse the get_db() function from user.py
# In a larger project, you'd put get_db() in a separate db.py file.
# For this learning project, importing it from user.py is fine.


class Category:
    """
    Represents a task category (e.g., "Work", "Personal").
    """

    def __init__(self, id, name, color, user_id):
        self.id = id
        self.name = name
        self.color = color
        self.user_id = user_id

    @staticmethod
    def create(name, user_id, color='#3498db'):
        """
        Create a new category in the database.
        
        Parameters:
            name (str): Category name, e.g., "Work"
            user_id (int): The ID of the user who owns this category
            color (str): Hex color code (default: blue)
        
        Returns: a Category object
        
        🔑 What is a default parameter?
        color='#3498db' means: if no color is provided, use '#3498db'.
        
        Category.create("Work", 1)              → color will be '#3498db'
        Category.create("Work", 1, '#e74c3c')   → color will be '#e74c3c'
        """
        db = get_db()

        cursor = db.execute(
            'INSERT INTO categories (name, color, user_id) VALUES (?, ?, ?)',
            (name, color, user_id)
        )
        db.commit()

        return Category(cursor.lastrowid, name, color, user_id)

    @staticmethod
    def get_all_by_user(user_id):
        """
        Get ALL categories belonging to a specific user.
        
        Returns: a list of Category objects.
        
        This is used to populate the category dropdown/filter in the frontend.
        """
        db = get_db()

        rows = db.execute(
            'SELECT * FROM categories WHERE user_id = ? ORDER BY name ASC',
            (user_id,)
        ).fetchall()
        """
        ORDER BY name ASC
        
        ORDER BY → sort the results
        name → sort by the "name" column
        ASC → ascending order (A → Z)
        
        DESC would be descending (Z → A).
        This ensures categories always appear in alphabetical order.
        """

        return [
            Category(row['id'], row['name'], row['color'], row['user_id'])
            for row in rows
        ]
        """
        🔑 What is a list comprehension?
        
        This is a shorthand way to create a list in Python.
        
        The long way (loop):
            result = []
            for row in rows:
                category = Category(row['id'], row['name'], row['color'], row['user_id'])
                result.append(category)
            return result
        
        The short way (list comprehension):
            return [Category(...) for row in rows]
        
        Both do exactly the same thing. List comprehensions are more "Pythonic"
        (the style that experienced Python developers prefer).
        """

    @staticmethod
    def find_by_id(category_id, user_id):
        """
        Find a specific category by ID, but ONLY if it belongs to the given user.
        
        Why check user_id too?
        Security! Without it, a user could access another user's categories
        by guessing the ID. We always filter by user_id to prevent this.
        
        This is called "authorization" — ensuring users can only access THEIR data.
        """
        db = get_db()

        row = db.execute(
            'SELECT * FROM categories WHERE id = ? AND user_id = ?',
            (category_id, user_id)
        ).fetchone()

        if row:
            return Category(row['id'], row['name'], row['color'], row['user_id'])
        return None

    @staticmethod
    def update(category_id, user_id, name=None, color=None):
        """
        Update a category's name and/or color.
        
        Parameters with None default:
            name=None means "if not provided, don't change the name."
            color=None means "if not provided, don't change the color."
        
        This allows partial updates:
            Category.update(1, 1, name="Office")        → only changes name
            Category.update(1, 1, color="#ff0000")       → only changes color
            Category.update(1, 1, name="Office", color="#ff0000")  → changes both
        """
        db = get_db()

        # First, check if the category exists and belongs to this user
        category = Category.find_by_id(category_id, user_id)
        if not category:
            return None

        # Use the new values if provided, otherwise keep the old ones
        updated_name = name if name is not None else category.name
        updated_color = color if color is not None else category.color
        """
        This is a conditional expression (Python's ternary operator):
        value_if_true IF condition ELSE value_if_false
        
        In JavaScript, the same thing looks like:
        condition ? value_if_true : value_if_false
        """

        db.execute(
            'UPDATE categories SET name = ?, color = ? WHERE id = ? AND user_id = ?',
            (updated_name, updated_color, category_id, user_id)
        )
        db.commit()

        return Category(category_id, updated_name, updated_color, user_id)

    @staticmethod
    def delete(category_id, user_id):
        """
        Delete a category.
        
        Remember: in schema.sql, we set ON DELETE SET NULL for the
        category_id foreign key in the tasks table.
        So when a category is deleted, tasks in that category
        will have their category_id set to NULL (uncategorized),
        but the tasks themselves are NOT deleted.
        
        Returns: True if deleted, False if not found.
        """
        db = get_db()

        result = db.execute(
            'DELETE FROM categories WHERE id = ? AND user_id = ?',
            (category_id, user_id)
        )
        db.commit()

        return result.rowcount > 0
        """
        rowcount tells you how many rows were affected by the query.
        If 1 row was deleted → rowcount is 1 → 1 > 0 → True
        If no rows matched → rowcount is 0 → 0 > 0 → False
        """

    def to_dict(self):
        """
        Convert to a dictionary for JSON responses.
        """
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'user_id': self.user_id
        }