from pydantic import BaseModel


class PortfolioCurrencySummary(BaseModel):
    currency: str
    cash: float
    invested_value: float
    market_value: float | None
    unrealized_pnl: float | None
    priced_positions_count: int
    unpriced_positions_count: int

class PortfolioSummarySimple(BaseModel):
    Total_EUR: float
    Total_USD: float
    Total_invested_EUR: float
    Total_invested_USD: float
    Profit_EUR: float
    Profit_USD: float
    Percentage_profit_EUR: float
    Percentage_profit_USD: float

class PortfolioSummary(BaseModel):
    by_currency: list[PortfolioCurrencySummary]