from pydantic import BaseModel

class Position(BaseModel):
    symbol: str
    name: str
    quantity: float
    average_cost: float
    current_price: float
    unrealized_pln: float
    currency: str

class PositionRead(BaseModel):
    symbol: str
    quantity: float
    average_cost: float
    total_cost: float