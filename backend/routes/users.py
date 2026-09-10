from fastapi import APIRouter
from models import UserProfile
import database

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register_user(profile: UserProfile):
    return await database.register_user(profile.model_dump())

@router.get("/{email}")
async def get_user(email: str):
    return await database.get_user(email)
