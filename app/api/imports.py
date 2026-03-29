from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from app.schemas.imports import ImportTransactionsResponse
from app.services.import_service import import_transactions_from_csv
from app.db.deps import get_db

router = APIRouter(tags=["imports"])

@router.post("/import/transactions", response_model=ImportTransactionsResponse)
def import_transactions(
    file: UploadFile,
    db: Session = Depends(get_db),
    ) -> ImportTransactionsResponse:
    result = import_transactions_from_csv(db, file)
    return result