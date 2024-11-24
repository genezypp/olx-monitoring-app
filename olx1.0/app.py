from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from data_manager import get_all_profiles, create_profile, update_profile, delete_profile
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
async def profiles(request: Request):
    """
    Display profiles with the option to manage them.
    """
    profiles = get_all_profiles()
    return templates.TemplateResponse("profiles.html", {"request": request, "profiles": profiles})

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
    Add a new profile.
    """
    try:
        create_profile(name, keyword, min_price, max_price, location, category, condition)
        return RedirectResponse("/profiles", status_code=303)
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
    Edit an existing profile.
    """
    try:
        update_profile(profile_id, name, keyword, min_price, max_price, location, category, condition)
        return RedirectResponse("/profiles", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/profiles/{profile_id}/delete")
async def remove_profile(profile_id: int):
    """
    Delete an existing profile.
    """
    try:
        delete_profile(profile_id)
        return RedirectResponse("/profiles", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
