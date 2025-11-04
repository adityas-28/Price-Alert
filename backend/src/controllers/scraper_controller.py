# from src.services.bewakoof_scraper import scrap_bewakoof

# def scrape_product(asin: str):
#     url = "https://www.bewakoof.com/p/" + asin
    
#     try:
#         result = scrap_bewakoof(url)
#         return {"status": "success", "data": result}
#     except Exception as e:
#         return {"status": "error", "message": f"Error Scraping - {url}: {str(e)}"}

from src.services.tanishq_scraper import scrap_tanishq 

def scrape_product(asin: str):
    """
    Scrapes product details from Tanishq based on SKU or product identifier.
    Example SKU: '50e5b1fck2a02'
    """
    url = f"https://www.tanishq.co.in/product/{asin}"

    try:
        result = scrap_tanishq(url)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": f"Error Scraping - {url}: {str(e)}"}
