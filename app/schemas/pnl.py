from tokenize import Floatnumber
from pydantic import BaseModel
from sqlalchemy.util import symbol

class PnLSummary(BaseModel):
    unrealized_pnl: float
    daily_pnl: float
    total_return_pct: float
    currency: str

class PnLRead(BaseModel):
    symbol: str
    quantity: float
    average_cost: float
    current_price: float
    market_value: float
    total_cost: float
    unrealized_pnl: float
    unrealized_pnl_percent: float