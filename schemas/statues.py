import sqlite3

conn = sqlite3.connect("db.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS statues(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES orders(id)
    FOREIGN KEY (name) REFERENCES invoices(id)
);    
""")
conn.commit()