import sqlite3

conn = sqlite3.connect("db.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_user_id INTEGER,
    date_create INTEGER,
    status_id INTEGER,
    invoice_id TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);    
""")
conn.commit()