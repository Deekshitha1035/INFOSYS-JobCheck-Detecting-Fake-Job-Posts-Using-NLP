import sqlite3

conn = sqlite3.connect("flags.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_text TEXT,
    reason TEXT,
    comments TEXT,
    email TEXT,
    timestamp TEXT
)
""")
conn.commit()

def store_flag(data):
    cursor.execute("""
    INSERT INTO flags (job_text, reason, comments, email, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["job_text"],
        data["reason"],
        data["comments"],
        data["email"],
        data["timestamp"]
    ))
    conn.commit()
