/*
   🔑 KEY CONCEPT: What is a Schema?

A schema is the STRUCTURE of your database — it defines:
- What tables exist (like spreadsheets)
- What columns each table has (like spreadsheet headers)
- What type of data each column holds (text, number, date, etc.)
- Rules about the data (required? unique? linked to another table?)

Think of it like an architect's blueprint:
Before building a house, you draw the plan.
Before storing data, you define the schema.


🔑 What is SQL?
SQL (Structured Query Language) is the language used to talk to databases.
- CREATE TABLE → build a new table
- INSERT INTO  → add a row
- SELECT       → read data
- UPDATE       → change data
- DELETE       → remove data

SQLite reads this file and creates the tables when the app starts.
*/


/* ──────────────────────────────────────────────
TABLE: users
Stores registered user accounts.
────────────────────────────────────────────── */

CREATE TABLE IF NOT EXISTS users (
/*
"CREATE TABLE IF NOT EXISTS" means:
- Create this table
- But ONLY if it doesn't already exist
- If it already exists, skip (don't crash)
This is important because this file runs every time the app starts.
*/

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    /*
      id: A unique number for each user (1, 2, 3, ...)

      INTEGER        → the data type (a whole number)
      PRIMARY KEY    → this column uniquely identifies each row
                       (no two users can have the same id)
      AUTOINCREMENT  → the database assigns the number automatically
                       (first user gets 1, next gets 2, etc.)
                       You never set this yourself.
    */

    username TEXT NOT NULL UNIQUE,
    /*
      username: The user's chosen name (e.g., "alice")

      TEXT      → the data type (a string of characters)
      NOT NULL  → this field is REQUIRED (can't be empty)
      UNIQUE    → no two users can have the same username
                  If someone tries to register "alice" twice, the database
                  will reject it with an error.
    */

    email TEXT NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,
    /*
      password_hash: The user's password, but ENCRYPTED.

      🔑 KEY CONCEPT: Why "hash" and not "password"?
      
      NEVER store passwords in plain text!
      If a hacker steals your database, they'd see everyone's passwords.

      Instead, we store a "hash" — a one-way scrambled version:
        "secret123" → "$2b$12$LJ3m4ys9Kq..."

      "One-way" means: you can turn a password INTO a hash,
      but you can NEVER turn a hash back into a password.

      To verify a login, we hash what the user typed and compare
      it to the stored hash. If they match → correct password.
    */

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    /*
      created_at: When the account was created.

      TIMESTAMP            → a date+time value (e.g., "2026-04-18 14:30:00")
      DEFAULT              → if no value is provided, use a default
      CURRENT_TIMESTAMP    → the default is "right now" (the moment the row is inserted)

      This is useful for knowing when users signed up, sorting by date, etc.
    */
);


/* ──────────────────────────────────────────────
TABLE: categories
Stores task categories (like "Work", "Personal", "Shopping").
Each category belongs to a specific user.
────────────────────────────────────────────── */

CREATE TABLE IF NOT EXISTS categories (
id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,
    /*
      The category name, e.g., "Work", "Personal", "Urgent"
    */

    color TEXT DEFAULT '#3498db',
    /*
      A hex color code for the category badge.
      DEFAULT '#3498db' means if no color is specified, use blue.

      🔑 What is a hex color?
      Colors on screens are made of Red, Green, Blue (RGB).
      Each is a value from 00 (none) to FF (maximum) in hexadecimal.

      #FF0000 = pure red    (max red, no green, no blue)
      #00FF00 = pure green
      #0000FF = pure blue
      #3498db = a nice medium blue
      #FFFFFF = white (all max)
      #000000 = black (all zero)
    */

    user_id INTEGER NOT NULL,
    /*
      Which user this category belongs to.
      This links the category to a specific user.
    */

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    /*
      🔑 KEY CONCEPT: Foreign Key

      A foreign key is a LINK between two tables.
      It says: "user_id in THIS table must match an id in the users table."

      This enforces data integrity:
      - You can't create a category for a user that doesn't exist.
      - The database will reject it with an error.

      ON DELETE CASCADE means:
      "If a user is DELETED, automatically delete ALL their categories too."
      
      Without CASCADE, you'd have orphaned categories (belonging to nobody).

      Think of it like: if a company closes, all its departments close too.
    */
);


/* ──────────────────────────────────────────────
TABLE: tasks
Stores the actual to-do items.
Each task belongs to a user and optionally to a category.
────────────────────────────────────────────── */

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,
    /*
      The task description, e.g., "Buy groceries"
      NOT NULL means you can't create a task without a title.
    */

    description TEXT DEFAULT '',

is_completed BOOLEAN DEFAULT 0,
    /*
      Whether the task is done or not.

      SQLite doesn't have a real BOOLEAN type — it uses INTEGER.
      0 = false (not completed)
      1 = true (completed)
      
      DEFAULT 0 means new tasks start as "not completed."
    */

    priority TEXT DEFAULT 'medium',
    due_date TEXT,

    category_id INTEGER,
    /*
      Which category this task belongs to (optional).
      
      Notice there's NO "NOT NULL" here — this field IS allowed to be empty (NULL).
      A task doesn't HAVE to belong to a category.
      NULL in databases means "no value" or "unknown."
    */

    user_id INTEGER NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
    /*
      ON DELETE SET NULL means:
      "If a category is deleted, set category_id to NULL (instead of deleting the task)."

      This is different from CASCADE:
      - CASCADE: delete the child too (used for users → categories)
      - SET NULL: keep the child but remove the link (used for categories → tasks)

      If you delete the "Work" category, the tasks that were in "Work"
      still exist — they just become uncategorized (category_id = NULL).
    */
);