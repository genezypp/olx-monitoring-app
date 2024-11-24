import sqlite3
from common.config import DATABASE_URL

def execute_query(query, params=None):
    """Execute a query on the database."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    return results

def init_db():
    """Initialize the database with the necessary tables."""
    create_ads_table()
    create_search_profiles_table()

def create_ads_table():
    """Create the ads table if it doesn't exist."""
    query = '''
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL,
        location TEXT,
        date_added TEXT,
        description TEXT
    )
    '''
    execute_query(query)

def create_search_profiles_table():
    """Create the search_profiles table if it doesn't exist."""
    query = '''
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
    '''
    execute_query(query)
