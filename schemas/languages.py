import sqlite3

conn = sqlite3.connect("db.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS languages(
    id TEXT PRIMARY KEY AUTOINCREMENT,
    language_code TEXT,
    FOREIGN KEY (language_code) REFERENCES bot_users(id)
);    
""")
conn.commit()