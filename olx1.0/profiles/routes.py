from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from profiles.services import (
    get_all_profiles,
    create_profile,
    update_profile,
    delete_profile,
)
from common.database import execute_query

profiles_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@profiles_router.get("/")
async def list_profiles(request: Request):
    profiles = get_all_profiles()
    return templates.TemplateResponse("profiles.html", {"request": request, "profiles": profiles})

@profiles_router.post("/")
async def add_profile(name: str, keyword: str, min_price: float, max_price: float, category: str, condition: str):
    create_profile(name, keyword, min_price, max_price, category, condition)
    return {"message": "Profile added successfully."}
