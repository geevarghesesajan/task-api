import sqlite3

# This is the file where SQLite saves all data permanently
DB_NAME = "tasks.db"

def get_db():
    """Connect to SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    # Allows us to access columns by name like task["title"] instead of task[1]
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Stage 0: Create the table and add initial tasks if empty."""
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

    # 2. Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    # 3. Insert 3 default tasks ONLY if table is empty
    if count == 0:
        initial_tasks = [
            ("Learn SQLite", False),
            ("Connect FastAPI to database", False),
            ("Build awesome CRUD API", True),
        ]
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)", 
            initial_tasks
        )
        conn.commit()

    conn.close()
