from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from data_manager import fetch_filtered_ads, get_all_profiles, create_profile, update_profile, delete_profile
from database import init_db

# Inicjalizacja bazy danych
init_db()

# Tworzenie instancji FastAPI
app = FastAPI()

# Konfiguracja plik�w statycznych
app.mount("/static", StaticFiles(directory="static"), name="static")

# Konfiguracja szablon�w Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Strona g��wna aplikacji."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ads", response_class=HTMLResponse)
async def show_ads(request: Request,
                   keyword: str = Query(None),
                   min_price: float = Query(None),
                   max_price: float = Query(None),
                   location: str = Query(None)):
    """Wy�wietla og�oszenia z bazy danych z filtrowaniem."""
    ads = fetch_filtered_ads(keyword, min_price, max_price, location)
    return templates.TemplateResponse("ads.html", {"request": request, "ads": ads})

@app.get("/profiles", response_class=HTMLResponse)
async def manage_profiles(request: Request):
    """Wy�wietla stron� zarz�dzania profilami wyszukiwania."""
    profiles = get_all_profiles()
    return templates.TemplateResponse("profiles.html", {"request": request, "profiles": profiles})

@app.post("/profiles")
async def add_profile(name: str, keyword: str = None, min_price: float = None, max_price: float = None, location: str = None):
    """Dodaje nowy profil wyszukiwania."""
    profile_id = create_profile(name, keyword, min_price, max_price, location)
    if not profile_id:
        raise HTTPException(status_code=400, detail="Failed to create profile")
    return RedirectResponse("/profiles", status_code=303)

@app.post("/profiles/{profile_id}/delete")
async def delete_profile_action(profile_id: int):
    """Usuwa profil wyszukiwania."""
    success = delete_profile(profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return RedirectResponse("/profiles", status_code=303)
