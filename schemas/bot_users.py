import sqlite3

conn = sqlite3.connect("db.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS bot_users(
    id TEXT PRIMARY KEY AUTOINCREMENT,
    is_blocked BOOLEAN DEFAULT (false),
    balance INTEGER,
    language_id INTEGER,
    FOREIGN KEY (balance) REFERENCES orders(id)
);    
""")
conn.commit()