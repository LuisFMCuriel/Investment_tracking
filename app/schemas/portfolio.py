from pydantic import BaseModel

class PortfolioSummary(BaseModel):
    total_value: float
    cash: float
    invested_value: float
    unrealized_pln: float
    currency: str
