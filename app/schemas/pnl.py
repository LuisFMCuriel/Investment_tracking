from pydantic import BaseModel

class PnLSummary(BaseModel):
    unrealized_pnl: float
    daily_pnl: float
    total_return_pct: float
    currency: str