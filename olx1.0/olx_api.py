import requests

API_BASE_URL = "https://api.olx.pl"  # U¿yj odpowiedniego URL z dokumentacji OLX
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Wstaw poprawny token dostêpu

def fetch_categories():
    """
    Fetch categories from the OLX API.
    Returns a list of categories or raises an exception on failure.
    """
    url = f"{API_BASE_URL}/categories"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch categories: {response.status_code}, {response.text}")
