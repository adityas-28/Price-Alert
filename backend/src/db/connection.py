import os
from datetime import datetime, timezone
from typing import Dict, Any
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from config import MONGO_URI

load_dotenv()
client = MongoClient(MONGO_URI)

db = client["priceAlert_db"]
products_collection = db["products"]
users_collection = db["users"]
alert_collection = db["alerts"]

def upsert_product(product: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update and Insert a product by ASIN and append price with timestamp.

    Expected product keys: asin (str), name (str), url (str), price (number)
    Stores:
      - asin, name, url
      - prices: array of { price, timestamp }
      - last_updated: ISO timestamp string
    """
    asin = product.get("asin")
    name = product.get("name")
    url = product.get("url")
    price = product.get("price")

    if not asin:
        raise ValueError("asin is required for upsert_product")

    now_iso = datetime.now(timezone.utc).isoformat()

    update_doc = {
        "$set": {
            "asin": asin,
            "name": name,
            "url": url,
            "last_updated": now_iso,
        },
        "$push": {
            "prices": {
                "price": price,
                "timestamp": now_iso,
            }
        },
        "$setOnInsert": {
            "created_at": now_iso,
        },
    }

    result = products_collection.find_one_and_update( # find_one_and_update is used to update the document if it exists, else create a new document
        {"asin": asin},
        update_doc, 
        upsert=True, # upsert is True, so if the document does not exist, it will be created
        return_document=ReturnDocument.AFTER, # return the updated document
    )

    # If None is returned (older pymongo), fetch the updated document
    if result is None:
        result = products_collection.find_one({"asin": asin})

    return result