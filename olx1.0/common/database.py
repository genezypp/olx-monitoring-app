import sqlite3
from config import DATABASE_URL

def execute_query(query, params=None):
    """Wykonuje zapytanie SQL na bazie danych."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        return results
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        conn.close()
