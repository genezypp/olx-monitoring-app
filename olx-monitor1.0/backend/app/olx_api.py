import requests
from decouple import config

BASE_URL = config("OLX_API_BASE_URL")
AUTH_URL = config("OLX_AUTH_URL")
TOKEN_URL = config("OLX_TOKEN_URL")
CLIENT_ID = config("OLX_CLIENT_ID")
CLIENT_SECRET = config("OLX_CLIENT_SECRET")

class OLXAPIClient:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None

    def authenticate(self, authorization_code=None):
        """Authenticate and get tokens."""
        data = {
            "grant_type": "authorization_code" if authorization_code else "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        if authorization_code:
            data["code"] = authorization_code
            data["redirect_uri"] = "http://localhost:8000/callback"  # Example redirect URI
        else:
            data["scope"] = "v2 read write"

        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        tokens = response.json()
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens.get("refresh_token")

    def refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            raise ValueError("No refresh token available")

        data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": self.refresh_token,
        }
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        tokens = response.json()
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens.get("refresh_token")

    def get(self, endpoint, params=None):
        """Send a GET request to the OLX API."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params)
        if response.status_code == 401:  # Token expired
            self.refresh_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

# Example Usage:
# olx_client = OLXAPIClient()
# olx_client.authenticate(authorization_code="your_code_here")
# categories = olx_client.get("categories")
