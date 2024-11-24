from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import jwt

# Tworzenie instancji aplikacji FastAPI
app = FastAPI()

# Montowanie plików statycznych
app.mount("/static", StaticFiles(directory="frontend/public/src"), name="static")

# Fake database for demonstration
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": "fakehashedpassword",  # Replace with hashed passwords in production
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your_secret_key"  # Replace with a secure key

class User(BaseModel):
    username: str

class SearchProfile(BaseModel):
    id: int
    name: str
    keyword: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    location: Optional[str] = None
    category: Optional[str] = None

# Tymczasowa baza danych dla profili wyszukiwania
search_profiles = []

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
async def get_profiles():
    """Pobiera listê wszystkich profili wyszukiwania."""
    return search_profiles

@app.post("/profiles", response_model=SearchProfile)
async def create_profile(profile: SearchProfile):
    """Tworzy nowy profil wyszukiwania."""
    search_profiles.append(profile)
    return profile

@app.put("/profiles/{profile_id}", response_model=SearchProfile)
async def update_profile(profile_id: int, updated_profile: SearchProfile):
    """Aktualizuje istniej¹cy profil wyszukiwania."""
    for i, profile in enumerate(search_profiles):
        if profile.id == profile_id:
            search_profiles[i] = updated_profile
            return updated_profile
    raise HTTPException(status_code=404, detail="Profile not found")

@app.delete("/profiles/{profile_id}")
async def delete_profile(profile_id: int):
    """Usuwa profil wyszukiwania."""
    global search_profiles
    search_profiles = [p for p in search_profiles if p.id != profile_id]
    return {"message": "Profile deleted successfully"}
