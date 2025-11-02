from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from src.models.alert_model import ProductAlert, UserAlert
from src.db.connection import alert_collection

router = APIRouter()

class AddAlertRequest(BaseModel):
    asin: str
    email: EmailStr
    threshold_price: float

@router.post("/add")
async def add_alert(request: AddAlertRequest):
    asin = request.asin
    email = request.email
    threshold_price = request.threshold_price
    existing = alert_collection.find_one({"asin": asin})

    if existing:
        # check if user already exists
        for user in existing["users"]:
            if user["email"] == email:
                raise HTTPException(status_code=400, detail="User already tracking this product")

        # add new user to the array
        alert_collection.update_one(
            {"asin": asin},
            {"$push": {"users": {"email": email, "threshold_price": threshold_price}}}
        )
        return {"message": "Added new user alert for existing product"}
    
    # create new product alert document
    new_alert = {
        "asin": asin,
        "users": [{"email": email, "threshold_price": threshold_price}]
    }
    result = alert_collection.insert_one(new_alert)
    return {"message": "New product alert created", "id": str(result.inserted_id)}
