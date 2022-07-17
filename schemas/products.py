import sqlite3

conn = sqlite3.connect("db.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    price REAL DEFAULT (0),
    media TEXT NOT NULL,
    total INTEGER DEFAULT (0),
    is_published BOOLEAN DEFAULT (false),
    name_en TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);    
""")
conn.commit()