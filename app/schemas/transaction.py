from datetime import date
from pydantic import BaseModel, Field, model_validator, ConfigDict, field_validator
from app.schemas.enums import TransactionType

class TransactionBase(BaseModel):
    symbol: str | None = None
    transaction_type: TransactionType
    quantity: float | None = None
    price: float | None = None
    amount: float | None = None
    currency: str
    fees: float = Field(default=0.0, ge=0)
    transaction_date: date

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip().upper()
        return value or None

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        value = value.strip().upper()
        if not value:
            raise ValueError("Currency is required")
        return value

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
            if self.quantity <= 0:
                raise ValueError("Quantity must be greater than 0 for BUY and SELL transactions")
            if self.price <= 0:
                raise ValueError("Price must be greater than 0 for BUY and SELL transactions")
            if self.amount is None:
                raise ValueError("Amount is required for BUY and SELL transactions")

        elif self.transaction_type in cash_types:
            if self.amount is None:
                raise ValueError("Amount is required for DIVIDEND, DEPOSIT, WITHDRAWAL, INTEREST, REWARD, and DISTRIBUTION transactions")
            if self.amount <= 0:
                raise ValueError("Amount must be greater than 0 for DIVIDEND, DEPOSIT, WITHDRAWAL, INTEREST, REWARD, and DISTRIBUTION transactions")
            if self.quantity is not None:
                raise ValueError("Quantity should not be provided for DIVIDEND, DEPOSIT, WITHDRAWAL, INTEREST, REWARD, and DISTRIBUTION transactions")
            if self.transaction_type in {TransactionType.DEPOSIT,
                                         TransactionType.WITHDRAWAL,
                                         TransactionType.INTEREST,
                                         TransactionType.REWARD} and self.symbol is not None:
                raise ValueError("Symbol should not be provided for DEPOSIT, WITHDRAWAL, INTEREST, and REWARD transactions")
            if self.transaction_type in {TransactionType.DIVIDEND, 
                                         TransactionType.DISTRIBUTION} and self.symbol is None:
                raise ValueError("Symbol is required for DIVIDEND and DISTRIBUTION transactions")
        return self
# What client sends
class TransactionCreate(TransactionBase):
    pass
# What API returns
class TransactionRead(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)