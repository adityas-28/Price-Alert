from fastapi import HTTPException, status
from src.db.connection import users_collection
from utils.auth import hash_password, verify_password, create_access_token
from models.user_model import UserRegister, UserLogin
from bson import ObjectId

async def register_user(user: UserRegister):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if user.email is None:
        raise HTTPException(status_code=400, detail="Email is required")

    if user.username is None:
        raise HTTPException(status_code=400, detail="Username is required")

    if user.password is None:
        raise HTTPException(status_code=400, detail="Password is required")

    if user.confirm_password is None:
        raise HTTPException(status_code=400, detail="Confirm password is required")
        
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_pw
    }

    result = users_collection.insert_one(new_user)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

async def login_user(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}
