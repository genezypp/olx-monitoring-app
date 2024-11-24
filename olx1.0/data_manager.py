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
        }
        for row in rows
    ]

def create_profile(name, keyword=None, min_price=None, max_price=None, location=None, category=None):
    """Create a new search profile."""
    query = """
        INSERT INTO search_profiles (name, keyword, min_price, max_price, location, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    params = (name, keyword, min_price, max_price, location, category)
    execute_query(query, params)

def update_profile(profile_id, name, keyword=None, min_price=None, max_price=None, location=None, category=None):
    """Update an existing search profile."""
    query = """
        UPDATE search_profiles
        SET name = ?, keyword = ?, min_price = ?, max_price = ?, location = ?, category = ?
        WHERE id = ?
    """
    params = (name, keyword, min_price, max_price, location, category, profile_id)
    execute_query(query, params)

def delete_profile(profile_id):
    """Delete a search profile."""
    query = "DELETE FROM search_profiles WHERE id = ?"
    execute_query(query, (profile_id,))

def get_market_depth(profile_id, range_size):
    """Calculate market depth for a given profile."""
    query = "SELECT min_price, max_price FROM search_profiles WHERE id = ?"
    profile = execute_query(query, (profile_id,))
    if not profile:
        raise ValueError("Profile not found.")
    
    min_price = profile[0][0]
    max_price = profile[0][1]
    query = """
        SELECT price FROM ads
        WHERE price >= ? AND price <= ?
    """
    ads = execute_query(query, (min_price, max_price))
    price_ranges = {}
    for ad in ads:
        price = ad[0]
        range_start = int(price // range_size) * range_size
        range_end = range_start + range_size
        range_key = f"{range_start}-{range_end}"
        price_ranges[range_key] = price_ranges.get(range_key, 0) + 1
    return [{"range": k, "count": v} for k, v in price_ranges.items()]
