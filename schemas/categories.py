import sqlite3

conn = sqlite3.connect("db.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    is_published BOOLEAN DEFAULT (false),
    name_en TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);    
""")
conn.commit()