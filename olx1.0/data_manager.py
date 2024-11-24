from database import execute_query

def fetch_ads():
    """Pobierz wszystkie ogloszenia z bazy danych."""
    query = "SELECT * FROM ads"
    ads = execute_query(query)
    return [{"id": ad[0], "title": ad[1], "price": ad[2], "location": ad[3], "date_added": ad[4]} for ad in ads]

def save_ad(title, price, location, date_added):
    """Zapisz ogloszenie w bazie danych."""
    query = "INSERT INTO ads (title, price, location, date_added) VALUES (?, ?, ?, ?)"
    execute_query(query, (title, price, location, date_added))
