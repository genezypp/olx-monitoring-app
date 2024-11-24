from common.database import execute_query

def analyze_market_depth(profile_id, interval):
    query = "SELECT * FROM ads WHERE profile_id=?"
    ads = execute_query(query, (profile_id,))
    
    # Analiza g³êbokoœci rynku
    price_ranges = {}
    for ad in ads:
        price = ad['price']
        range_start = int(price / interval) * interval
        range_key = f"{range_start}-{range_start + interval - 1}"
        price_ranges[range_key] = price_ranges.get(range_key, 0) + 1

    return price_ranges
