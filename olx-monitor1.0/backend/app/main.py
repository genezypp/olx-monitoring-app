from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

import jwt

app = FastAPI()

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

    @app.get("/")
async def root():
    return {"message": "Welcome to the OLX Monitor API"}

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/public/index.html", "r") as file:
        return file.read()