from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PriceEntry(BaseModel):
    price: Optional[str] = None
    timestamp: Optional[datetime] = None

class product_mode(BaseModel):
    asin: str
    name: str
    url: str
    prices: list[PriceEntry]
    created_at: datetime
    last_updated: datetime