from sqlalchemy.orm import Session
from app.services.transaction_service import create_transaction, transaction_exists
from app.schemas.imports import ImportTransactionsResponse
import csv
from app.services.importers.lightyear_importer import map_lightyear_row_to_transaction


def import_transactions_from_csv(db: Session,
                                 file) -> ImportTransactionsResponse:
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(content.splitlines())
    created = 0
    skipped = 0
    errors = []
    
    for i, row in enumerate(reader, start=2):
        try:
            transaction_data = map_lightyear_row_to_transaction(row)

            if not transaction_data:
                skipped += 1
                errors.append(
                    {
                        "row": i,
                        "error": "Unsupported Lightyear Type - skipped: " + row["Type"].strip()
                    }
                )
                continue
            if transaction_exists(db, transaction_data):
                skipped += 1
                errors.append(
                    {
                        "row": i,
                        "error": "Duplicate transaction - skipped: " + row["Type"].strip()
                    }
                )
                continue
            create_transaction(db, transaction_data)
            created += 1
        except Exception as e:
            db.rollback()
            errors.append(
                {
                    "row": i,
                    "error": f"Row {i+1}: {str(e)}, type: {row.get('Type', '').strip()}"
                }
            )
    return ImportTransactionsResponse(
        created=created,
        skipped=skipped,
        errors=errors
    )