import httpx
from config import API_BASE_URL

async def fetch_price(asin: str) -> float:
    url = f"{API_BASE_URL}/api/scraper/scrap/{asin}"
    timeout = httpx.Timeout(5.0, read=30.0)
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()  # Raise if error
            json_data = resp.json()

            try:
                price_str = json_data["data"]["Price"][0]
                return float(price_str)
            except (KeyError, IndexError, ValueError, TypeError):
                return 0.0
    except httpx.TimeoutException:
        print(f"Timeout while fetching price for {asin}")
        return 0.0
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code} for {asin}: {e.response.text}")
        return 0.0
    except Exception as e:
        print(f"Error fetching price for {asin}: {str(e)}")
        return 0.0 