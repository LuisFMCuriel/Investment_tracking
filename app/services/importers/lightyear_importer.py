from datetime import datetime

from app.schemas.enums import TransactionType
from app.schemas.transaction import TransactionCreate


LIGHTYEAR_TYPE_MAP = {
    "Buy": TransactionType.BUY,
    "Sell": TransactionType.SELL,
    "Dividend": TransactionType.DIVIDEND,
    "Deposit": TransactionType.DEPOSIT,
    "Withdrawal": TransactionType.WITHDRAWAL,
    "Interest": TransactionType.INTEREST,
    "Reward": TransactionType.REWARD,
    "Distribution": TransactionType.DISTRIBUTION,
}


SKIPPED_LIGHTYEAR_TYPES = {"Conversion"}


def parse_lightyear_date(raw_value: str):
    return datetime.strptime(raw_value.strip(), "%d/%m/%Y %H:%M:%S").date()


def parse_optional_float(raw_value: str | None) -> float | None:
    if raw_value is None:
        return None

    value = raw_value.strip()
    if value == "":
        return None

    return float(value)


def map_lightyear_row_to_transaction(row: dict) -> TransactionCreate | None:
    raw_type = row["Type"].strip()

    if raw_type in SKIPPED_LIGHTYEAR_TYPES:
        return None

    if raw_type not in LIGHTYEAR_TYPE_MAP:
        raise ValueError(f"Unsupported Lightyear Type: {raw_type}")

    transaction_type = LIGHTYEAR_TYPE_MAP[raw_type]
    symbol = row["Ticker"].strip().upper() if row.get("Ticker") else None
    currency = row["CCY"].strip().upper()
    fees = parse_optional_float(row.get("Fee")) or 0.0
    transaction_date = parse_lightyear_date(row["Date"])

    if transaction_type in {TransactionType.BUY, TransactionType.SELL}:
        return TransactionCreate(
            symbol=symbol,
            transaction_type=transaction_type,
            quantity=parse_optional_float(row.get("Quantity")),
            price=parse_optional_float(row.get("Price/share")),
            amount=parse_optional_float(row.get("Net Amt.")),
            currency=currency,
            fees=fees,
            transaction_date=transaction_date,
        )

    return TransactionCreate(
        symbol=symbol,
        transaction_type=transaction_type,
        quantity=None,
        price=None,
        amount=parse_optional_float(row.get("Net Amt.")),
        currency=currency,
        fees=fees,
        transaction_date=transaction_date,
    )