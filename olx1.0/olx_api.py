import requests
from requests.auth import HTTPBasicAuth
from config import OLX_API_URL, CLIENT_ID, CLIENT_SECRET

class OLXAPIClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = OLX_API_URL
        self.token = self.get_access_token()

    def get_access_token(self):
        """Uzyskuje token dostêpu u¿ywaj¹c OAuth 2.0."""
        url = f"{self.base_url}/oauth/token"
        data = {
            "grant_type": "client_credentials"
        }
        try:
            response = requests.post(
                url,
                data=data,
                auth=HTTPBasicAuth(self.client_id, self.client_secret)
            )
            response.raise_for_status()
            token_info = response.json()
            return token_info.get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining access token: {e}")
            return None

    def get_headers(self):
        """Zwraca nag³ówki wymagane przez OLX API."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def fetch_ads(self, query_params=None):
        """
        Pobiera og³oszenia z OLX API.
        :param query_params: S³ownik z parametrami zapytania, np. {"category_id": 1}
        :return: Lista og³oszeñ w formacie JSON.
        """
        url = f"{self.base_url}/ads"
        headers = self.get_headers()
        try:
            response = requests.get(url, headers=headers, params=query_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ads: {e}")
            return None

# Przyk³adowe u¿ycie modu³u
if __name__ == "__main__":
    client = OLXAPIClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    ads = client.fetch_ads({"category_id": 1})
    print(ads)
