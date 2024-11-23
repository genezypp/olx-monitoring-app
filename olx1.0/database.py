import sqlite3

def create_database():
    conn = sqlite3.connect("olx_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY,
            title TEXT,
            price REAL,
            location TEXT,
            date_added TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
