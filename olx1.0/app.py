from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from data_manager import (
    get_all_profiles,
    create_profile,
    update_profile,
    delete_profile,
    fetch_profile_ads,
)
from olx_api import fetch_categories_test

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    """
    Main page displaying all profiles.
    """
    try:
        profiles = get_all_profiles()
        return templates.TemplateResponse("profiles.html", {"request": request, "profiles": profiles})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categories")
async def get_categories():
    """
    Endpoint to fetch categories (test data for now).
    """
    try:
        categories = fetch_categories_test()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/profiles")
async def add_profile(
    name: str = Form(...),
    keyword: str = Form(None),
    min_price: float = Form(None),
    max_price: float = Form(None),
    location: str = Form(None),
    category: str = Form(None),
    condition: str = Form(None),
):
    """
    Add a new search profile.
    """
    create_profile(name, keyword, min_price, max_price, location, category, condition)
    return {"message": "Profile created successfully"}


@app.get("/profiles/{profile_id}", response_class=HTMLResponse)
async def profile_detail(request: Request, profile_id: int):
    """
    Show details and market depth for a specific profile.
    """
    try:
        ads = fetch_profile_ads(profile_id)
        return templates.TemplateResponse(
            "profile_detail.html", {"request": request, "ads": ads, "profile_id": profile_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/profiles/{profile_id}/edit")
async def edit_profile(
    profile_id: int,
    name: str = Form(...),
    keyword: str = Form(None),
    min_price: float = Form(None),
    max_price: float = Form(None),
    location: str = Form(None),
    category: str = Form(None),
    condition: str = Form(None),
):
    """
    Edit an existing search profile.
    """
    update_profile(profile_id, name, keyword, min_price, max_price, location, category, condition)
    return {"message": "Profile updated successfully"}


@app.post("/profiles/{profile_id}/delete")
async def delete_profile_endpoint(profile_id: int):
    """
    Delete an existing search profile.
    """
    delete_profile(profile_id)
    return {"message": "Profile deleted successfully"}
