from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from data_manager import get_all_profiles, create_profile, update_profile, delete_profile, fetch_filtered_ads
from olx_api import fetch_categories_test  # Poprawiony import

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/categories")
async def get_categories():
    """
    Endpoint to fetch categories (test data for now).
    """
    try:
        categories = fetch_categories_test()  # Poprawiono na funkcjê fetch_categories_test
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profiles", response_class=HTMLResponse)
async def profiles(request: Request):
    """
    Display profiles with the option to manage them.
    """
    try:
        profiles = get_all_profiles()
        categories = fetch_categories_test()  # U¿ywamy danych testowych kategorii
        return templates.TemplateResponse(
            "profiles.html",
            {"request": request, "profiles": profiles, "categories": categories},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/profiles")
async def add_profile(
    name: str,
    keyword: str = None,
    min_price: float = None,
    max_price: float = None,
    location: str = None,
    category: str = None,
):
    """
    Add a new search profile.
    """
    create_profile(name, keyword, min_price, max_price, location, category)
    return {"message": "Profile created successfully"}


@app.post("/profiles/{profile_id}/edit")
async def edit_profile(
    profile_id: int,
    name: str,
    keyword: str = None,
    min_price: float = None,
    max_price: float = None,
    location: str = None,
    category: str = None,
):
    """
    Edit an existing search profile.
    """
    update_profile(profile_id, name, keyword, min_price, max_price, location, category)
    return {"message": "Profile updated successfully"}


@app.post("/profiles/{profile_id}/delete")
async def delete_profile_endpoint(profile_id: int):
    """
    Delete an existing search profile.
    """
    delete_profile(profile_id)
    return {"message": "Profile deleted successfully"}
