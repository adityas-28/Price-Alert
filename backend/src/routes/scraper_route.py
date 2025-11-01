from fastapi import APIRouter
from src.controllers.scraper_controller import scrape_product

router = APIRouter()

@router.get("/scrap/{asin}")
def scrap(asin: str):
    return scrape_product(asin)
