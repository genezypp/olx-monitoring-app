import os

# �cie�ka do pliku SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///olx_app.db")
