from fastapi import FastAPI
from profiles.routes import profiles_router
from ads.routes import ads_router

app = FastAPI()

# Rejestracja modu³ów
app.include_router(profiles_router, prefix="/profiles", tags=["Profiles"])
app.include_router(ads_router, prefix="/ads", tags=["Ads"])
