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

        try:
            current_price = await fetch_price(asin)
            notified_users = []

            # Only check price threshold if we successfully fetched a valid price
            if current_price > 0:
                for user in users:
                    if current_price <= user["threshold_price"]:
                        try:
                            await send_email(
                                to_email=user["email"],
                                asin=asin,
                                current_price=current_price,
                                threshold=user["threshold_price"]
                            )
                            notified_users.append(user["email"])
                        except Exception as e:
                            print(f"⚠️ Error sending email to {user['email']} for {asin}: {str(e)}")
                            # Continue with other users even if one email fails

            results.append({
                "asin": asin, 
                "current_price": current_price, 
                "notified": notified_users,
                "status": "success" if current_price > 0 else "failed"
            })
        except Exception as e:
            print(f"Error processing product {asin}: {str(e)}")
            results.append({
                "asin": asin,
                "current_price": 0.0,
                "notified": [],
                "status": "error",
                "error": str(e)
            })

    return {"message": "Scrape and notify completed", "results": results}
