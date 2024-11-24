from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from data_manager import get_all_profiles, create_profile, update_profile, delete_profile
from olx_api import fetch_categories_test

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Fetch categories (using test data)
@app.get("/categories")
async def get_categories():
    """
    Endpoint to fetch categories (using test data).
    """
    try:
        categories = fetch_categories_test()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Display profiles with management options
@app.get("/profiles", response_class=HTMLResponse)
async def profiles(request: Request):
    """
    Display profiles and manage them.
    """
    profiles = get_all_profiles()
    categories = fetch_categories_test()
    return templates.TemplateResponse("profiles.html", {"request": request, "profiles": profiles, "categories": categories})

# Add a new profile
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
    create_profile(name, keyword, min_price, max_price, location, category, condition)
    return RedirectResponse(url="/profiles", status_code=303)

# Edit an existing profile
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
    update_profile(profile_id, name, keyword, min_price, max_price, location, category, condition)
    return RedirectResponse(url="/profiles", status_code=303)

# Delete a profile
@app.post("/profiles/{profile_id}/delete")
async def remove_profile(profile_id: int):
    delete_profile(profile_id)
    return RedirectResponse(url="/profiles", status_code=303)
