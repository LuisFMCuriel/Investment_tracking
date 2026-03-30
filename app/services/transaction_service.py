from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


def create_transaction(db: Session, transaction_in: TransactionCreate) -> Transaction:
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
    return db.query(Transaction).all()

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