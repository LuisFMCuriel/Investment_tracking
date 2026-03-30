from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import date
from sqlalchemy import String, Float, Date, Enum
from app.schemas.enums import TransactionType
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), 
        nullable=False)
    quantity: Mapped[float | None] = mapped_column(Float, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String)
    fees: Mapped[float] = mapped_column(Float, default=0.0)
    transaction_date: Mapped[date] = mapped_column(Date)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    
    