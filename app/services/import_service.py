from sqlalchemy.orm import Session
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import create_transaction
import csv

def import_transactions_from_csv(db: Session,
                                 file) -> dict[str, str]:
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(content.splitlines())
    created = 0
    errors = []

    for i, row in enumerate(reader, start=2):
        try:
            transaction_data = TransactionCreate(
                symbol = row["symbol"],
                transaction_type = row["transaction_type"],
                quantity = float(row["quantity"]),
                price = float(row["price"]),
                currency = row["currency"],
                fees = float(row["fees"]),
                transaction_date = row["transaction_date"],
            )
            create_transaction(db, transaction_data)
            created += 1
        except Exception as e:
            errors.append(f"Row {i+1}: {str(e)}")
    return {"created": created, "errors": errors}