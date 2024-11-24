from common.database import execute_query

def get_all_profiles():
    query = "SELECT * FROM search_profiles"
    return execute_query(query)

def create_profile(name, keyword, min_price, max_price, category, condition):
    query = """
    INSERT INTO search_profiles (name, keyword, min_price, max_price, category, condition)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    params = (name, keyword, min_price, max_price, category, condition)
    execute_query(query, params)

def update_profile(profile_id, name, keyword, min_price, max_price, category, condition):
    query = """
    UPDATE search_profiles SET name=?, keyword=?, min_price=?, max_price=?, category=?, condition=?
    WHERE id=?
    """
    params = (name, keyword, min_price, max_price, category, condition, profile_id)
    execute_query(query, params)

def delete_profile(profile_id):
    query = "DELETE FROM search_profiles WHERE id=?"
    execute_query(query, (profile_id,))
