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

cur.execute("""
CREATE TABLE IF NOT EXISTS order_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    total INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(id)
);    
""")
conn.commit()

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

cur.execute("""
CREATE TABLE IF NOT EXISTS statues(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES orders(id)
    FOREIGN KEY (name) REFERENCES invoices(id)
);    
""")
conn.commit()

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

cur.execute("""
CREATE TABLE IF NOT EXISTS languages(
    id TEXT PRIMARY KEY AUTOINCREMENT,
    language_code TEXT,
    FOREIGN KEY (language_code) REFERENCES bot_users(id)
);    
""")
conn.commit()

conn.close()