from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import jwt

from backend.app.db import engine, Base, get_db
from backend.app.models import SearchProfile as DBSearchProfile, Listing as DBListing
from backend.app.olx_api import OLXAPIClient  # Import klienta OLX API

# Tworzenie instancji aplikacji FastAPI
app = FastAPI()

# Montowanie plików statycznych
app.mount("/static", StaticFiles(directory="frontend/public/src"), name="static")

# Tworzenie tabel w bazie danych
Base.metadata.create_all(bind=engine)

# Fake database for demonstration
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": "fakehashedpassword",  # Replace with hashed passwords in production
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_secret_key"  # Replace with a secure key

olx_client = OLXAPIClient()  # Inicjalizacja klienta OLX API


class User(BaseModel):
    username: str


class SearchProfile(BaseModel):
    id: Optional[int] = None
    name: str
    keyword: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    location: Optional[str] = None
    category: Optional[str] = None

    class Config:
        orm_mode = True


class Listing(BaseModel):
    id: Optional[int] = None
    title: str
    price: Optional[float] = None
    link: str
    location: Optional[str] = None
    category: Optional[str] = None

    class Config:
        orm_mode = True


@app.post("/token")
async def login(form_data: dict):
    username = form_data.get("username")
    password = form_data.get("password")
    user = fake_users_db.get(username)
    if not user or user["hashed_password"] != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        return {"username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("frontend/public/index.html", "r") as file:
            return file.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>Frontend file not found</h1>", status_code=404)


# Endpointy CRUD dla profili wyszukiwania
@app.get("/profiles", response_model=List[SearchProfile])
async def get_profiles(db: Session = Depends(get_db)):
    return db.query(DBSearchProfile).all()


@app.post("/profiles", response_model=SearchProfile)
async def create_profile(profile: SearchProfile, db: Session = Depends(get_db)):
    db_profile = DBSearchProfile(**profile.dict(exclude_unset=True))
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@app.put("/profiles/{profile_id}", response_model=SearchProfile)
async def update_profile(profile_id: int, updated_profile: SearchProfile, db: Session = Depends(get_db)):
    db_profile = db.query(DBSearchProfile).filter(DBSearchProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in updated_profile.dict(exclude_unset=True).items():
        setattr(db_profile, key, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@app.delete("/profiles/{profile_id}")
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(DBSearchProfile).filter(DBSearchProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(db_profile)
    db.commit()
    return {"message": "Profile deleted successfully"}


@app.get("/auth")
async def authenticate():
    """Redirects the user to the OLX authentication page."""
    return {"auth_url": olx_client.get_auth_url()}


@app.get("/callback")
async def callback(request: Request):
    """Handles the OAuth callback and exchanges the authorization code for a token."""
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    try:
        olx_client.authenticate(authorization_code=code)
        return {"message": "Authenticated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profiles/{profile_id}/listings", response_model=List[Listing])
async def get_listings_for_profile(profile_id: int, db: Session = Depends(get_db)):
    """Fetches and saves listings from OLX API based on a search profile."""
    profile = db.query(DBSearchProfile).filter(DBSearchProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    params = {
        "keyword": profile.keyword,
        "min_price": profile.min_price,
        "max_price": profile.max_price,
        "location": profile.location,
        "category": profile.category,
    }

    try:
        listings = olx_client.get_listings(params)
        saved_listings = []
        for listing in listings:
            if not db.query(DBListing).filter(DBListing.link == listing["link"]).first():
                new_listing = DBListing(
                    title=listing["title"],
                    price=listing.get("price"),
                    link=listing["link"],
                    location=listing.get("location"),
                    category=listing.get("category"),
                    profile_id=profile_id,
                )
                db.add(new_listing)
                saved_listings.append(new_listing)
        db.commit()
        return saved_listings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
