from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import date
from sqlalchemy import String, Float, Date, Column, Enum as SqlEnum
from app.schemas.enums import TransactionType
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String, index=True)
    transaction_type: Column(SqlEnum(TransactionType), nullable=False)
    quantity: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String)
    fees: Mapped[float] = mapped_column(Float, default=0.0)
    transaction_date: Mapped[date] = mapped_column(Date)