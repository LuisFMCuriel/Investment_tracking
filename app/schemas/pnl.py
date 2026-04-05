from tokenize import Floatnumber
from pydantic import BaseModel
from sqlalchemy.util import symbol

class PnLSummary(BaseModel):
    unrealized_pnl: float
    daily_pnl: float
    total_return_pct: float
    currency: str

class PnlRead(BaseModel):
    symbol: str
    quantity: float
    currency: str
    average_cost: float
    current_price: float | None
    market_value: float | None
    total_cost: float
    unrealized_pnl: float | None
    unrealized_pnl_percent: float | None
    price_available: bool
    price_currency: str | None = None
    provider: str | None = None