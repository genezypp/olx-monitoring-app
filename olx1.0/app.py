from fastapi import HTTPException
from data_manager import (
    get_all_profiles,
    create_profile,
    update_profile,
    delete_profile
)

@app.get("/profiles")
async def list_profiles():
    """Zwraca wszystkie profile wyszukiwania."""
    return get_all_profiles()

@app.post("/profiles")
async def add_profile(name: str, keyword: str = None, min_price: float = None, max_price: float = None, location: str = None):
    """Dodaje nowy profil wyszukiwania."""
    profile_id = create_profile(name, keyword, min_price, max_price, location)
    if not profile_id:
        raise HTTPException(status_code=400, detail="Failed to create profile")
    return {"message": "Profile created", "id": profile_id}

@app.put("/profiles/{profile_id}")
async def modify_profile(profile_id: int, name: str, keyword: str = None, min_price: float = None, max_price: float = None, location: str = None):
    """Aktualizuje istniejacy profil wyszukiwania."""
    success = update_profile(profile_id, name, keyword, min_price, max_price, location)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile updated"}

@app.delete("/profiles/{profile_id}")
async def remove_profile(profile_id: int):
    """Usuwa istniejacy profil wyszukiwania."""
    success = delete_profile(profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted"}
