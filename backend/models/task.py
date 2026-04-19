"""
models/task.py — Task Data Access Layer

WHAT IS A DATA ACCESS LAYER?
It's a collection of functions that handle ALL database operations for tasks.
Routes NEVER write SQL directly — they call these functions instead.

WHY?
1. If you change the database structure, you only fix code in ONE place
2. You can reuse the same query in multiple routes
3. You can test database logic separately from HTTP logic
4. Routes stay clean and readable

This pattern is sometimes called a DAO (Data Access Object) or Repository pattern.
"""

from database import get_db


class TaskModel:
    """All database operations related to tasks."""

    @staticmethod
    def create(title, description, priority, due_date, category_id, user_id):
        """
        Insert a new task into the database.

        Returns the newly created task as a dictionary.
        """
        db = get_db()
        cursor = db.execute(
            """INSERT INTO tasks (title, description, priority, due_date, category_id, user_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (title, description, priority, due_date, category_id, user_id)
            # Remember: ALWAYS use ? placeholders, NEVER f-strings!
        )
        db.commit()
        # cursor.lastrowid gives us the auto-generated ID of the new row
        return TaskModel.get_by_id(cursor.lastrowid, user_id)

    @staticmethod
    def get_all(user_id, filters=None):
        """
        Get all tasks for a specific user, optionally filtered.

        Parameters:
            user_id: The ID of the logged-in user
            filters: Optional dict like {"is_completed": "1", "priority": "high"}

        Returns a list of task dictionaries.

        NOTE: We always filter by user_id. This is CRITICAL for security!
        User A must NEVER be able to see User B's tasks.
        """
        # We build the SQL query DYNAMICALLY based on which filters are provided
        query = "SELECT * FROM tasks WHERE user_id = ?"
        params = [user_id]
        #   params is a list — we'll pass it to db.execute()
        #   The ? placeholders in the query get replaced with these values SAFELY

        # Add optional filters
        if filters:
            if filters.get("is_completed") is not None:
                query += " AND is_completed = ?"
                params.append(int(filters["is_completed"]))

            if filters.get("priority"):
                query += " AND priority = ?"
                params.append(filters["priority"])

            if filters.get("category_id"):
                query += " AND category_id = ?"
                params.append(int(filters["category_id"]))

        query += " ORDER BY created_at DESC"
        #   DESC = descending (newest first)

        db = get_db()
        rows = db.execute(query, params).fetchall()
        #   fetchall() returns ALL matching rows
        #   Each row is a sqlite3.Row object (thanks to our row_factory)

        return [dict(row) for row in rows]
        #   Convert sqlite3.Row objects to regular Python dictionaries
        #   so Flask can easily convert them to JSON

    @staticmethod
    def get_by_id(task_id, user_id):
        """
        Get a single task by its ID.

        Returns a dict if found, None if not found.

        NOTE: We check BOTH task_id AND user_id. This prevents a user
        from accessing another user's task by guessing the ID!
        """
        db = get_db()
        row = db.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()
        #   fetchone() returns ONE row (or None if no match)

        return dict(row) if row else None

    @staticmethod
    def update(task_id, user_id, data):
        """
        Update a task with new values.

        Parameters:
            task_id: Which task to update
            user_id: The logged-in user (for security)
            data: Dict of fields to update, e.g. {"title": "New title", "priority": "high"}

        Returns the updated task, or None if not found.
        """
        # WHITELIST: Only allow these specific fields to be updated.
        # This prevents attackers from modifying fields they shouldn't
        # (like user_id or created_at) by sending extra data.
        allowed_fields = ['title', 'description', 'is_completed', 'priority', 'due_date', 'category_id']
        fields = {key: value for key, value in data.items() if key in allowed_fields}

        if not fields:
            return TaskModel.get_by_id(task_id, user_id)

        # Build the SET clause dynamically:  "title = ?, priority = ?"
        set_clause = ", ".join(f"{key} = ?" for key in fields)
        values = list(fields.values()) + [task_id, user_id]

        db = get_db()
        db.execute(
            f"UPDATE tasks SET {set_clause}, updated_at = CURRENT_TIMESTAMP "
            f"WHERE id = ? AND user_id = ?",
            values
        )
        db.commit()
        return TaskModel.get_by_id(task_id, user_id)

    @staticmethod
    def delete(task_id, user_id):
        """
        Delete a task.

        Returns True if a task was deleted, False if it wasn't found.
        """
        db = get_db()
        cursor = db.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
        db.commit()

        # cursor.rowcount tells us how many rows were affected
        # If it's 0, the task didn't exist (or didn't belong to this user)
        return cursor.rowcount > 0