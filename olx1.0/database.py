import sqlite3
from config import DATABASE_URL

def init_db():
    """Inicjalizuje baze danych."""
    create_ads_table()
    create_search_profiles_table()

def create_ads_table():
    """Tworzy tabele ads, jesli nie istnieje."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            location TEXT,
            date_added TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_search_profiles_table():
    """Tworzy tabele search_profiles, jesli nie istnieje."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            keyword TEXT,
            min_price REAL,
            max_price REAL,
            location TEXT,
            category TEXT,
            condition TEXT
        )
    ''')
    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Wykonuje zapytanie SQL na bazie danych."""
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
