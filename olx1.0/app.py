from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from data_manager import fetch_filtered_ads

# Tworzenie instancji FastAPI
app = FastAPI()

# Ustawienia Jinja2
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
