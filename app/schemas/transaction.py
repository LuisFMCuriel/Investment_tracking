from datetime import date
from pydantic import BaseModel, Field
from app.schemas.enums import TransactionType
# What client sends
class TransactionCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    transaction_type: TransactionType
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    fees: float = Field(default=0, ge=0)
    transaction_date: date
# What API returns
class TransactionRead(BaseModel):
    id: int
    symbol: str
    transaction_type: TransactionType
    quantity: float
    price: float
    currency: str
    fees: float
    transaction_date: date

    model_config = {
        "from_attributes": True
    }