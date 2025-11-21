from fastapi import APIRouter, HTTPException
from src.db.connection import products_collection  

router = APIRouter()

@router.get("/{asin}")
async def get_product_by_asin(asin: str):
    product = products_collection.find_one({"asin": asin})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product["_id"] = str(product["_id"])

    return product
