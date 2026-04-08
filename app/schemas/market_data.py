from datetime import datetime

from pydantic import BaseModel


class MarketQuote(BaseModel):
    symbol: str
    price: float | None = None
    currency: str | None = None
    exchange: str | None = None
    as_of: datetime | None = None
    provider: str
    price_available: bool = False