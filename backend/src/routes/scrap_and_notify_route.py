from fastapi import APIRouter
from datetime import datetime
from src.db.connection import alert_collection, products_collection
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
                            print(f"Error sending email to {user['email']} for {asin}: {str(e)}")
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

@router.get("/scrap-products")
async def update_all_products():
    """
    Scrape all products from the products_collection,
    update their current prices, and append them to the prices array.
    """
    products = products_collection.find({}).to_list(None)
    results = []

    for product in products:
        asin = product.get("asin")
        url = product.get("url")

        try:
            # Fetch latest price using existing utility
            current_price = await fetch_price(asin)

            if current_price and float(current_price) > 0:
                new_price_entry = {
                    "price": str(current_price),
                    "timestamp": datetime.utcnow().isoformat()
                }

                # Append new price entry to prices array
                products_collection.update_one(
                    {"_id": product["_id"]},
                    {
                        "$push": {"prices": new_price_entry},
                        "$set": {"last_updated": datetime.utcnow().isoformat()}
                    }
                )

                results.append({
                    "asin": asin,
                    "price": current_price,
                    "status": "updated"
                })
            else:
                results.append({
                    "asin": asin,
                    "price": None,
                    "status": "failed"
                })

        except Exception as e:
            print(f"Error updating {asin}: {str(e)}")
            results.append({
                "asin": asin,
                "error": str(e),
                "status": "error"
            })

    return {"message": "Product price update completed", "results": results}