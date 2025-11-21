from fastapi import APIRouter
from datetime import datetime
from src.db.connection import alert_collection, products_collection
from src.utils.scraper import fetch_price
from src.utils.notifier import send_email

router = APIRouter()

@router.get("/scrap-all")
async def scrap_and_notify():
    # Fetch all alerts from database
    alerts = alert_collection.find({}).to_list(None)
    
    # Group alerts by ASIN to avoid duplicate scraping
    # Key: asin, Value: list of all users tracking this ASIN
    asin_to_users = {}
    
    for alert in alerts:
        asin = alert.get("asin")
        users = alert.get("users", [])
        
        if not asin:
            continue
            
        # If ASIN already exists, merge users (handle duplicates)
        if asin in asin_to_users:
            # Add users that aren't already in the list (deduplicate by email)
            existing_emails = {user["email"] for user in asin_to_users[asin]}
            for user in users:
                if user.get("email") not in existing_emails:
                    asin_to_users[asin].append(user)
        else:
            asin_to_users[asin] = users.copy()
    
    results = []
    
    # Process each unique ASIN only once
    for asin, users in asin_to_users.items():
        try:
            # Fetch price only once per ASIN
            current_price = await fetch_price(asin)
            notified_users = []

            # Only check price threshold if we successfully fetched a valid price
            if current_price > 0:
                for user in users:
                    threshold_price = user.get("threshold_price", 0)
                    if current_price <= threshold_price:
                        try:
                            await send_email(
                                to_email=user["email"],
                                asin=asin,
                                current_price=current_price,
                                threshold=threshold_price
                            )
                            notified_users.append(user["email"])
                        except Exception as e:
                            print(f"Error sending email to {user['email']} for {asin}: {str(e)}")
                            # Continue with other users even if one email fails

            results.append({
                "asin": asin, 
                "current_price": current_price, 
                "notified": notified_users,
                "users_count": len(users),
                "status": "success" if current_price > 0 else "failed"
            })
        except Exception as e:
            print(f"Error processing product {asin}: {str(e)}")
            results.append({
                "asin": asin,
                "current_price": 0.0,
                "notified": [],
                "users_count": len(users),
                "status": "error",
                "error": str(e)
            })

    return {"message": "Scrape and notify completed", "results": results}

@router.get("/scrap-products")
async def update_all_products():
    """
    Scrape all products from the products_collection,
    update their current prices, and append them to the prices array.
    Groups products by ASIN to avoid duplicate scraping.
    """
    # Fetch all products from database
    products = products_collection.find({}).to_list(None)
    
    # Group products by ASIN to avoid duplicate scraping
    # Key: asin, Value: list of product documents with that ASIN
    asin_to_products = {}
    
    for product in products:
        asin = product.get("asin")
        
        if not asin:
            continue
            
        # Group products by ASIN
        if asin in asin_to_products:
            asin_to_products[asin].append(product)
        else:
            asin_to_products[asin] = [product]
    
    results = []
    
    # Process each unique ASIN only once
    for asin, product_list in asin_to_products.items():
        try:
            # Fetch price only once per ASIN
            current_price = await fetch_price(asin)
            updated_count = 0
            failed_count = 0

            if current_price and float(current_price) > 0:
                new_price_entry = {
                    "price": str(current_price),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                # Update all products with this ASIN
                for product in product_list:
                    try:
                        # Append new price entry to prices array for each product document
                        products_collection.update_one(
                            {"_id": product["_id"]},
                            {
                                "$push": {"prices": new_price_entry},
                                "$set": {"last_updated": datetime.utcnow().isoformat()}
                            }
                        )
                        updated_count += 1
                    except Exception as e:
                        print(f"Error updating product document {product.get('_id')} for ASIN {asin}: {str(e)}")
                        failed_count += 1

                results.append({
                    "asin": asin,
                    "price": current_price,
                    "products_updated": updated_count,
                    "products_failed": failed_count,
                    "total_products": len(product_list),
                    "status": "updated" if updated_count > 0 else "failed"
                })
            else:
                results.append({
                    "asin": asin,
                    "price": None,
                    "products_updated": 0,
                    "products_failed": len(product_list),
                    "total_products": len(product_list),
                    "status": "failed"
                })

        except Exception as e:
            print(f"Error processing ASIN {asin}: {str(e)}")
            results.append({
                "asin": asin,
                "error": str(e),
                "products_updated": 0,
                "products_failed": len(product_list),
                "total_products": len(product_list),
                "status": "error"
            })

    return {"message": "Product price update completed", "results": results}