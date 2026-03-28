from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


def create_transaction(db: Session, transaction_in: TransactionCreate) -> Transaction:
    transaction = Transaction(
        symbol=transaction_in.symbol,
        transaction_type=transaction_in.transaction_type,
        quantity=transaction_in.quantity,
        price=transaction_in.price,
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