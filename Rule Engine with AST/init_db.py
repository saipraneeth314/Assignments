import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('rules.db')
c = conn.cursor()

# Create a table to store rules
c.execute('''CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_string TEXT NOT NULL
            )''')

# Create a table to store metadata
c.execute('''CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL
            )''')

# Commit the changes and close the connection
conn.commit()
conn.close()
