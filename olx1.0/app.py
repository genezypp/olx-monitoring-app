from fastapi import Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from data_manager import fetch_filtered_ads

templates = Jinja2Templates(directory="templates")

@app.get("/ads", response_class=HTMLResponse)
async def show_ads(request: Request,
                   keyword: str = Query(None),
                   min_price: float = Query(None),
                   max_price: float = Query(None),
                   location: str = Query(None)):
    """Wyœwietla og³oszenia z bazy z mo¿liwoœci¹ filtrowania."""
    ads = fetch_filtered_ads(keyword, min_price, max_price, location)
    return templates.TemplateResponse("ads.html", {"request": request, "ads": ads})
