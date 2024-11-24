from database import execute_query

def get_all_profiles():
    """Retrieve all search profiles."""
    query = "SELECT * FROM search_profiles"
    rows = execute_query(query)
    return [
        {
            "id": row[0],
            "name": row[1],
            "keyword": row[2],
            "min_price": row[3],
            "max_price": row[4],
            "location": row[5],
            "category": row[6],
            "condition": row[7],
        }
        for row in rows
    ]

def create_profile(name, keyword=None, min_price=None, max_price=None, location=None, category=None, condition=None):
    """Create a new search profile."""
    query = """
    INSERT INTO search_profiles (name, keyword, min_price, max_price, location, category, condition)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = (name, keyword, min_price, max_price, location, category, condition)
    execute_query(query, params)

def update_profile(profile_id, name, keyword=None, min_price=None, max_price=None, location=None, category=None, condition=None):
    """Update an existing search profile."""
    query = """
    UPDATE search_profiles
    SET name = ?, keyword = ?, min_price = ?, max_price = ?, location = ?, category = ?, condition = ?
    WHERE id = ?
    """
    params = (name, keyword, min_price, max_price, location, category, condition, profile_id)
    execute_query(query, params)

def delete_profile(profile_id):
    """Delete a search profile."""
    query = "DELETE FROM search_profiles WHERE id = ?"
    execute_query(query, (profile_id,))
