def get_all_profiles():
    """Pobiera wszystkie profile wyszukiwania."""
    query = "SELECT * FROM search_profiles"
    rows = execute_query(query)
    return [{"id": row[0], "name": row[1], "keyword": row[2], "min_price": row[3], "max_price": row[4], "location": row[5]} for row in rows]

def create_profile(name, keyword=None, min_price=None, max_price=None, location=None):
    """Tworzy nowy profil wyszukiwania."""
    query = "INSERT INTO search_profiles (name, keyword, min_price, max_price, location) VALUES (?, ?, ?, ?, ?)"
    params = (name, keyword, min_price, max_price, location)
    execute_query(query, params)
    return True

def update_profile(profile_id, name, keyword=None, min_price=None, max_price=None, location=None):
    """Aktualizuje istniejacy profil wyszukiwania."""
    query = """
    UPDATE search_profiles
    SET name = ?, keyword = ?, min_price = ?, max_price = ?, location = ?
    WHERE id = ?
    """
    params = (name, keyword, min_price, max_price, location, profile_id)
    execute_query(query, params)
    return True

def delete_profile(profile_id):
    """Usuwa profil wyszukiwania."""
    query = "DELETE FROM search_profiles WHERE id = ?"
    execute_query(query, (profile_id,))
    return True
