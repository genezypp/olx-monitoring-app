import sqlite3
from config import DATABASE_URL

def seed_data():
    """Populate the database with test data."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Add test profiles
    cursor.executemany(
        '''
        INSERT INTO search_profiles (name, keyword, min_price, max_price, location, category, condition)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        [
            ("Profile 1", "iPhone", 500, 1000, "Warsaw", "electronics/phones", "new"),
            ("Profile 2", "Samsung Galaxy", 700, 1500, "Krakow", "electronics/phones", "used"),
            ("Profile 3", "Laptop", 1500, 3000, "Gdansk", "electronics/laptops", "damaged"),
        ]
    )

    # Add test ads
    cursor.executemany(
        '''
        INSERT INTO ads (title, price, location, date_added, description)
        VALUES (?, ?, ?, ?, ?)
        ''',
        [
            ("iPhone 12", 800, "Warsaw", "2024-11-23", "Brand new iPhone 12"),
            ("Samsung Galaxy S21", 1200, "Krakow", "2024-11-22", "Used Samsung Galaxy S21"),
            ("Dell Inspiron Laptop", 2000, "Gdansk", "2024-11-20", "Damaged Dell Inspiron laptop"),
        ]
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_data()
