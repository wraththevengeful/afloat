import sqlite3

def init_db(db_name="afloat.db"):
    """Creates the necessary tables for Afloat."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create tasks table
    # Handles both one-off tasks and recurring habits via 'frequency'
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            frequency TEXT DEFAULT 'once',  -- 'once', 'daily', 'weekly'
            status TEXT DEFAULT 'pending',  -- 'pending', 'completed'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Database '{db_name}' initialized successfully.")

if __name__ == "__main__":
    init_db()