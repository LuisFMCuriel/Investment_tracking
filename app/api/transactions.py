from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.services.transaction_service import create_transaction, get_transactions

router = APIRouter(tags=["transactions"])


@router.post(
    "/transactions",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction_endpoint(
    transaction_in: TransactionCreate,
    db: Session = Depends(get_db),
) -> TransactionRead:
    transaction = create_transaction(db, transaction_in)
    return transaction

@router.get("/transactions", response_model=list[TransactionRead])
def read_transactions_endpoint(db: Session = Depends(get_db)) -> list[TransactionRead]:
    transactions = get_transactions(db)
    return transactions