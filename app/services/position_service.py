from app.schemas.position import PositionRead
from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.transaction import Transaction
from app.schemas.enums import TransactionType

def get_positions(db: Session) -> list[PositionRead]:
    transactions = db.query(Transaction).order_by(Transaction.transaction_date, Transaction.id).all()
    positions = defaultdict(lambda: {"quantity": 0, "total_cost": 0.0})

    for tx in transactions:
        if tx.transaction_type not in {TransactionType.BUY, TransactionType.SELL}:
            continue
        # Here we are basically removing transactions like dividends, reward, distribution, etc.
        if not tx.symbol:
            continue
        key = (tx.symbol, tx.currency)
        quantity = tx.quantity or 0.0
        price = tx.price or 0.0
        fees = tx.fees or 0.0

        if tx.transaction_type == TransactionType.BUY:
            positions[key]["quantity"] += quantity
            positions[key]["total_cost"] += (quantity * price) + fees
        
        elif tx.transaction_type == TransactionType.SELL:
            current_quantity = positions[key]["quantity"]
            current_total_cost = positions[key]["total_cost"]

            if current_quantity <= 0:
                continue
            average_cost = current_total_cost / current_quantity
            positions[key]["quantity"] -= quantity
            positions[key]["total_cost"] -= average_cost * quantity

            #if positions[key]["quantity"] < 0:
            #    positions[key]["quantity"] = 0.0
            #    positions[key]["total_cost"] = 0.0

    results = []
    for (symbol, currency), data in positions.items():
        quantity = data["quantity"]
        total_cost = data["total_cost"]

        if quantity <= 0:
            continue

        average_cost = total_cost / quantity if quantity > 0 else 0.0
        results.append(PositionRead(
            symbol=symbol,
            currency=currency,
            quantity=round(quantity,6),
            average_cost=round(average_cost, 2),
            total_cost=round(total_cost, 2)
        ))

    results.sort(key=lambda x: x.symbol)
    return results