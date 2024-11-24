def create_search_profiles_table():
    """Tworzy tabele dla profili wyszukiwania, jesli nie istnieje."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            keyword TEXT,
            min_price REAL,
            max_price REAL,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Zaktualizuj funkcjê init_db, aby uwzglêdnia³a now¹ tabelê:
def init_db():
    """Inicjalizuje baze danych."""
    create_ads_table()
    create_search_profiles_table()
