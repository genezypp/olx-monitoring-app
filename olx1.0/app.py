from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from data_manager import get_all_profiles, create_profile, update_profile, delete_profile, fetch_filtered_ads
from olx_api import fetch_categories
from database import init_db, execute_query

app = FastAPI()

# Initialize database
init_db()

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
async def profiles(request: Request):
    """
    Display profiles with the option to manage them.
    """
    profiles = get_all_profiles()
    categories = fetch_categories()
    return templates.TemplateResponse(
        "profiles.html", 
        {"request": request, "profiles": profiles, "categories": categories}
    )

@app.post("/profiles")
async def add_profile(
    name: str = Form(...),
    keyword: str = Form(None),
    min_price: float = Form(None),
    max_price: float = Form(None),
    location: str = Form(None),
    category: str = Form(...)
):
    """
    Add a new profile.
    """
    create_profile(name, keyword, min_price, max_price, location, category)
    return {"message": "Profile created successfully"}

@app.post("/profiles/{profile_id}/edit")
async def edit_profile(
    profile_id: int,
    name: str = Form(...),
    keyword: str = Form(None),
    min_price: float = Form(None),
    max_price: float = Form(None),
    location: str = Form(None),
    category: str = Form(...)
):
    """
    Edit an existing profile.
    """
    update_profile(profile_id, name, keyword, min_price, max_price, location, category)
    return {"message": "Profile updated successfully"}

@app.post("/profiles/{profile_id}/delete")
async def delete_profile_endpoint(profile_id: int):
    """
    Delete a profile.
    """
    delete_profile(profile_id)
    return {"message": "Profile deleted successfully"}

@app.get("/profiles/{profile_id}/depth", response_class=HTMLResponse)
async def profile_depth(request: Request, profile_id: int, range_step: int = 100):
    """
    View the market depth for a specific profile.
    """
    profile = [p for p in get_all_profiles() if p["id"] == profile_id]
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile = profile[0]

    ads = fetch_filtered_ads(profile["keyword"], profile["min_price"], profile["max_price"], profile["location"])
    ads_sorted = sorted(ads, key=lambda ad: ad["price"])
    depth = {}
    
    for ad in ads_sorted:
        price_range = (int(ad["price"] // range_step) * range_step, int(ad["price"] // range_step + 1) * range_step)
        if price_range not in depth:
            depth[price_range] = 0
        depth[price_range] += 1

    return templates.TemplateResponse(
        "market_depth.html", 
        {"request": request, "profile": profile, "depth": depth, "range_step": range_step}
    )
