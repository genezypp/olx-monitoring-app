from database import execute_query

def get_all_profiles():
    """
    Retrieve all search profiles.
    """
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


def fetch_profile_ads(profile_id):
    """
    Fetch ads for a specific profile.
    """
    query = "SELECT * FROM ads WHERE profile_id = ?"
    rows = execute_query(query, (profile_id,))
    return [
        {"title": row[1], "price": row[2], "location": row[3], "date_added": row[4]}
        for row in rows
    ]


def create_profile(name, keyword=None, min_price=None, max_price=None, location=None, category=None, condition=None):
    """
    Create a new search profile.
    """
    query = """
    INSERT INTO search_profiles (name, keyword, min_price, max_price, location, category, condition)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    execute_query(query, (name, keyword, min_price, max_price, location, category, condition))


def update_profile(profile_id, name, keyword=None, min_price=None, max_price=None, location=None, category=None, condition=None):
    """
    Update an existing search profile.
    """
    query = """
    UPDATE search_profiles
    SET name = ?, keyword = ?, min_price = ?, max_price = ?, location = ?, category = ?, condition = ?
    WHERE id = ?
    """
    execute_query(query, (name, keyword, min_price, max_price, location, category, condition, profile_id))


def delete_profile(profile_id):
    """
    Delete a search profile.
    """
    query = "DELETE FROM search_profiles WHERE id = ?"
    execute_query(query, (profile_id,))
