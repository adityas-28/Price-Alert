from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=30) # required and must be between 3 and 30 characters long
    email: EmailStr
    password: str = Field(..., min_length=6) # required and must be at least 6 characters long
    confirm_password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: str
    username: str
    email: EmailStr