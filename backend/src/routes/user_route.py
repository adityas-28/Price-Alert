from fastapi import APIRouter
from controllers.user_controller import register_user, login_user
from models.user_model import UserRegister, UserLogin

router = APIRouter(tags=["User"])

@router.post("/register")
async def register(user: UserRegister):
    return await register_user(user)

@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user)
