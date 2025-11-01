import sqlite3

def get_connection():
    return sqlite3.connect("shop.db")

def setup_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        description TEXT,
        category TEXT,
        type TEXT,
        photo TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        phone TEXT,
        location TEXT,
        payment TEXT,
        total INTEGER,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


import sqlite3

conn = sqlite3.connect("shop.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(products)")
columns = [info[1] for info in cur.fetchall()]
if "photo" not in columns:
    cur.execute("ALTER TABLE products ADD COLUMN photo TEXT")


conn.commit()
conn.close()

print("✅ photo ustuni muvaffaqiyatli qo‘shildi!")

