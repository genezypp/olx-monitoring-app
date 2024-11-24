from fastapi import APIRouter, Request
from ads.services import analyze_market_depth
from fastapi.templating import Jinja2Templates

ads_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@ads_router.get("/market-depth")
async def market_depth(request: Request, profile_id: int, interval: int = 100):
    depth_data = analyze_market_depth(profile_id, interval)
    return templates.TemplateResponse("market_depth.html", {"request": request, "depth_data": depth_data})
