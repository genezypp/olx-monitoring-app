import sqlite3
from config import DATABASE_URL

def init_db():
    """Initialize the database."""
    create_ads_table()
    create_search_profiles_table()

def create_ads_table():
    """Create the ads table if it doesn't exist."""
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
    """Create the search_profiles table if it doesn't exist."""
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
