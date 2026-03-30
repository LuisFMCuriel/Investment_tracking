from datetime import date
from pydantic import BaseModel, Field, model_validator, ConfigDict
from app.schemas.enums import TransactionType

class TransactionBase(BaseModel):
    symbol: str | None = None
    transaction_type: TransactionType | None = None
    quantity: float | None = None
    price: float | None = None
    amount: float | None = None
    currency: str
    fees: float = 0.0
    transaction_date: date

    @model_validator(mode = "after")
    def validate_transaction_fields(self):
        trade_types = {TransactionType.BUY, TransactionType.SELL}
        cash_types = {
            TransactionType.DIVIDEND, 
            TransactionType.DEPOSIT, 
            TransactionType.WITHDRAWAL,
            TransactionType.INTEREST,
            TransactionType.REWARD,
            TransactionType.DISTRIBUTION
        }
        if self.transaction_type in trade_types:
            if not self.symbol:
                raise ValueError("Symbol is required for BUY and SELL transactions")
            if self.quantity is None:
                raise ValueError("Quantity is required for BUY and SELL transactions")
            if self.price is None:
                raise ValueError("Price is required for BUY and SELL transactions")
        if self.transaction_type in cash_types:
            if self.amount is None:
                raise ValueError("Amount is required for DIVIDEND, DEPOSIT, WITHDRAWAL, INTEREST, REWARD, and DISTRIBUTION transactions")
        return self
# What client sends
class TransactionCreate(TransactionBase):
    pass
# What API returns
class TransactionRead(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
"""
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
    """