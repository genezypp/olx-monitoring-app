from database import execute_query

def fetch_filtered_ads(keyword=None, min_price=None, max_price=None, location=None):
    """Fetch ads from the database with optional filters."""
    query = "SELECT * FROM ads WHERE 1=1"
    params = []

    if keyword:
        query += " AND title LIKE ?"
        params.append(f"%{keyword}%")
    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    return [
        {"title": row[1], "price": row[2], "location": row[3], "date_added": row[4], "description": row[5]}
        for row in execute_query(query, params)
    ]

def get_all_profiles():
    """Retrieve all search profiles."""
    query = "SELECT * FROM search_profiles"
    rows = execute_query(query)
    return [{"id": row[0], "name": row[1], "keyword": row[2], "min_price": row[3], "max_price": row[4], "location": row[5]} for row in rows]

def create_profile(name, keyword=None, min_price=None, max_price=None, location=None):
    """Create a new search profile."""
    query = "INSERT INTO search_profiles (name, keyword, min_price, max_price, location) VALUES (?, ?, ?, ?, ?)"
    params = (name, keyword, min_price, max_price, location)
    execute_query(query, params)
    return True

def update_profile(profile_id, name, keyword=None, min_price=None, max_price=None, location=None):
    """Update an existing search profile."""
    query = """
    UPDATE search_profiles
    SET name = ?, keyword = ?, min_price = ?, max_price = ?, location = ?
    WHERE id = ?
    """
    params = (name, keyword, min_price, max_price, location, profile_id)
    execute_query(query, params)
    return True

def delete_profile(profile_id):
    """Delete a search profile."""
    query = "DELETE FROM search_profiles WHERE id = ?"
    execute_query(query, (profile_id,))
    return True
