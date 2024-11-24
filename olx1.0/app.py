from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from data_manager import get_all_profiles
from olx_api import fetch_categories

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/categories")
async def get_categories():
    """
    Endpoint to fetch categories from OLX API.
    """
    try:
        categories = fetch_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profiles", response_class=HTMLResponse)
async def profiles():
    """
    Display profiles with the option to manage them.
    """
    profiles = get_all_profiles()
    return templates.TemplateResponse("profiles.html", {"request": {}, "profiles": profiles})
