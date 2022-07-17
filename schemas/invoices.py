import sqlite3

conn = sqlite3.connect("db.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS invoices(
    id TEXT PRIMARY KEY AUTOINCREMENT,
    bot_user_id TEXT,
    date_create INTEGER,
    total INTEGER,
    status_id INTEGER,
    FOREIGN KEY (bot_user_id) REFERENCES orders(bot_user_id)
);    
""")
conn.commit()