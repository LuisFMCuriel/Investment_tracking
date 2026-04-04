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

            if positions[key]["quantity"] < 0:
                positions[key]["quantity"] = 0.0
                positions[key]["total_cost"] = 0.0

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






"""
def get_positions() -> list[Position]:
    # This is a placeholder implementation. In a real application, you would fetch this data from a database or an external API.
    return [
        Position(
            symbol="AAPL",
            name="Apple Inc.",
            quantity=10,
            average_cost=150.00,
            current_price=170.00,
            unrealized_pln=200.00,
            currency="USD"
        ),
        Position(
            symbol="GOOGL",
            name="Alphabet Inc.",
            quantity=5,
            average_cost=2500.00,
            current_price=2800.00,
            unrealized_pln=1500.00,
            currency="USD"
        ),
        Position(
            symbol="VWCE",
            name="Vanguard FTSE All-World UCITS ETF",
            quantity=8,
            average_cost=600.00,
            current_price=700.00,
            unrealized_pln=800.00,
            currency="EUR"
        )
    ]
    """