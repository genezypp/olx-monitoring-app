from fastapi import FastAPI
from profiles.routes import profiles_router
from ads.routes import ads_router

app = FastAPI()

# Rejestracja modu³ów
app.include_router(profiles_router, prefix="/profiles", tags=["Profiles"])
app.include_router(ads_router, prefix="/ads", tags=["Ads"])

@app.on_event("startup")
async def startup_event():
    try:
        conn = sqlite3.connect(DATABASE_URL)
        conn.execute("SELECT 1")
        conn.close()
        print("Database connection successful!")
    except sqlite3.Error as e:
        print(f"Failed to connect to database: {e}")
