from database import execute_query

def fetch_filtered_ads(keyword=None, min_price=None, max_price=None, location=None):
    """Pobierz ogloszenia z uwzglednieniem filtrow."""
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
