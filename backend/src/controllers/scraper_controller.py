from src.services.bewakoof_scraper import scrap_bewakoof

def scrape_product(asin: str):
    url = "https://www.bewakoof.com/p/" + asin
    
    try:
        result = scrap_bewakoof(url)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": f"Error Scraping - {url}: {str(e)}"}
