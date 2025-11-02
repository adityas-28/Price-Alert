import httpx

async def fetch_price(asin: str) -> float:
    url = f"http://127.0.0.1:8000/api/scraper/scrap/{asin}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        return float(data.get("price", 0))
