import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE jobs ADD COLUMN created_at TEXT")

conn.commit()
conn.close()

print("created_at column added")
