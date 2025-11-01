from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PriceAlert(BaseModel):
    user_email: str
    product_asin: str
    threshold_price: int
    # last_notified: Optional[datetime] = None
