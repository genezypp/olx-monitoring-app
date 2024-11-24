from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from data_manager import fetch_filtered_ads, get_all_profiles, create_profile, update_profile, delete_profile

# Tworzenie instancji FastAPI
app = FastAPI()

# Konfiguracja szablonow Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ads", response_class=HTMLResponse)
async def show_ads(request: Request,
                   keyword: str = Query(None),
                   min_price: float = Query(None),
                   max_price: float = Query(None),
                   location: str = Query(None)):
    ads = fetch_filtered_ads(keyword, min_price, max_price, location)
    return templates.TemplateResponse("ads.html", {"request": request, "ads": ads})

@app.get("/profiles")
async def list_profiles():
    """Zwraca wszystkie profile wyszukiwania."""
    return get_all_profiles()

@app.post("/profiles")
async def add_profile(name: str, keyword: str = None, min_price: float = None, max_price: float = None, location: str = None):
    """Dodaje nowy profil wyszukiwania."""
    profile_id = create_profile(name, keyword, min_price, max_price, location)
    if not profile_id:
        raise HTTPException(status_code=400, detail="Failed to create profile")
    return {"message": "Profile created", "id": profile_id}

@app.put("/profiles/{profile_id}")
async def modify_profile(profile_id: int, name: str, keyword: str = None, min_price: float = None, max_price: float = None, location: str = None):
    """Aktualizuje istniejacy profil wyszukiwania."""
    success = update_profile(profile_id, name, keyword, min_price, max_price, location)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile updated"}

@app.delete("/profiles/{profile_id}")
async def remove_profile(profile_id: int):
    """Usuwa istniejacy profil wyszukiwania."""
    success = delete_profile(profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted"}
