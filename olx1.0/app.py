from fastapi import FastAPI
from database import init_db
from data_manager import fetch_ads
from fastapi.responses import HTMLResponse
import config

app = FastAPI()

# Inicjalizacja bazy danych
init_db()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>OLX Monitoring</title></head>
    <body>
        <h1>OLX Monitoring App</h1>
        <p>Backend is running successfully!</p>
        <p>Visit /ads to see fetched ads.</p>
    </body>
    </html>
    """

@app.get("/ads")
async def get_ads():
    ads = fetch_ads()
    return {"ads": ads}
