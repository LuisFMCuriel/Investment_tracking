from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.schemas.enums import TransactionType


def get_owned_quantity(db: Session, symbol: str) -> float:
    stmt = (
        select(Transaction)
        .where(
            Transaction.symbol == symbol,
            Transaction.transaction_type.in_([TransactionType.BUY, TransactionType.SELL]),
        )
        .order_by(Transaction.transaction_date, Transaction.id)
    )
    transactions = db.execute(stmt).scalars().all()

    quantity = 0.0
    for tx in transactions:
        if tx.transaction_type == TransactionType.BUY:
            quantity += tx.quantity or 0.0
        elif tx.transaction_type == TransactionType.SELL:
            quantity -= tx.quantity or 0.0

    return quantity

def create_transaction(db: Session, transaction_in: TransactionCreate) -> Transaction:
    if transaction_exists(db, transaction_in):
        raise ValueError("This transaction already exists")

    if transaction_in.transaction_type == TransactionType.SELL:
        if transaction_in.symbol is None:
            raise ValueError("Symbol is required for SELL transactions")
        if transaction_in.quantity is None:
            raise ValueError("Quantity is required for SELL transactions")
        """
        owned_quantity = get_owned_quantity(db, transaction_in.symbol)
        if transaction_in.quantity > owned_quantity:
            raise ValueError(
                f"Cannot sell {transaction_in.quantity} of {transaction_in.symbol}; only {owned_quantity} available"
            )"""

    transaction = Transaction(
        symbol=transaction_in.symbol,
        transaction_type=transaction_in.transaction_type,
        quantity=transaction_in.quantity,
        price=transaction_in.price,
        amount=transaction_in.amount,
        currency=transaction_in.currency,
        fees=transaction_in.fees,
        transaction_date=transaction_in.transaction_date,
    )
    # Stage object
    db.add(transaction)
    # Save to dataset
    db.commit()
    # Reload object from db to get IDs
    db.refresh(transaction)

    return transaction

# latest transaction first, if same date then latest id first
def get_transactions(db: Session) -> list[Transaction]:
    stmt = select(Transaction).order_by(
        desc(Transaction.transaction_date),
        desc(Transaction.id),
    )
    return db.execute(stmt).scalars().all()

def transaction_exists(db: Session, transaction_in: TransactionCreate) -> bool:
    stmt = select(Transaction).where(
        Transaction.symbol == transaction_in.symbol,
        Transaction.transaction_type == transaction_in.transaction_type,
        Transaction.quantity == transaction_in.quantity,
        Transaction.price == transaction_in.price,
        Transaction.amount == transaction_in.amount,
        Transaction.currency == transaction_in.currency,
        Transaction.fees == transaction_in.fees,
        Transaction.transaction_date == transaction_in.transaction_date,
    )
    existing = db.execute(stmt).scalar_one_or_none()
    return existing is not None