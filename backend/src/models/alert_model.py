from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class UserAlert(BaseModel):
    email: EmailStr
    threshold_price: float

class ProductAlert(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    asin: str
    users: List[UserAlert] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "asin": "B09G9FPHYF",
                "users": [
                    {"email": "user1@example.com", "threshold_price": 499.99},
                    {"email": "user2@example.com", "threshold_price": 550.00}
                ]
            }
        }
