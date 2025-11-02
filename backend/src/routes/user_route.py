from fastapi import APIRouter, Response, Depends
from src.controllers.user_controller import register_user, login_user, logout_user
from src.models.user_model import UserRegister, UserLogin
from src.utils.auth import get_current_user

router = APIRouter()

@router.post("/register")
async def register(user: UserRegister):
    return await register_user(user)

@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user)

@router.post("/logout")
async def logout(response: Response, user_email: str = Depends(get_current_user)):
    return await logout_user(response, user_email)
