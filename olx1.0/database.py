import sqlite3
from config import DATABASE_URL

def init_db():
    """Inicjalizacja bazy danych."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL,
        location TEXT,
        date_added TEXT
    )
    """)
    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Wykonaj zapytanie SQL."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results
