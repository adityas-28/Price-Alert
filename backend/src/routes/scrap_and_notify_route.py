from fastapi import APIRouter
from src.db.connection import alert_collection
from src.utils.scraper import fetch_price
from src.utils.notifier import send_email

router = APIRouter()

@router.get("/scrap-all")
async def scrap_and_notify():
    products = alert_collection.find({}).to_list(None)
    results = []

    for product in products:
        asin = product["asin"]
        users = product["users"]

        current_price = await fetch_price(asin)
        notified_users = []

        for user in users:
            if current_price <= user["threshold_price"]:
                await send_email(
                    to_email=user["email"],
                    asin=asin,
                    current_price=current_price,
                    threshold=user["threshold_price"]
                )
                notified_users.append(user["email"])

        results.append({"asin": asin, "current_price": current_price, "notified": notified_users})

    return {"message": "Scrape and notify completed", "results": results}
