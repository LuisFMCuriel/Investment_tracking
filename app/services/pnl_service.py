from sqlalchemy.orm import Session

from app.schemas.pnl import PnlRead, PnLSummary
from app.services.market_data_service import market_data_service
from app.services.position_service import get_positions


def get_pnl_summary() -> PnLSummary:
    # Placeholder implementation - replace with actual logic to calculate PnL summary
    return PnLSummary(
        unrealized_pnl=240.00,
        daily_pnl=35.50,
        total_return_pct=4.12,
        currency="EUR"
    )

def get_pnl(db: Session) -> list[PnlRead]:
    positions = get_positions(db)
    results = []
    for pos in positions:
        try:
            quote = market_data_service.get_current_quote(pos.symbol, pos.currency)
        except ValueError:
            results.append(
                PnlRead(
                    symbol=pos.symbol,
                    currency=pos.currency,
                    quantity=round(pos.quantity, 6),
                    average_cost=round(pos.average_cost, 2),
                    current_price=None,
                    market_value=None,
                    total_cost=round(pos.total_cost, 2),
                    unrealized_pnl=None,
                    unrealized_pnl_percent=None,
                    price_available=False,
                    price_currency=None,
                    provider="twelve_data",
                )
            )
        continue

        # Only compute when quote exists
        if not quote.price_available or quote.price is None:
            results.append(
                PnlRead(
                    symbol = pos.symbol,
                    currency = pos.currency,
                    quantity = round(pos.quantity,6),
                    average_cost=round(pos.average_cost, 2),
                    current_price=None,
                    market_value=None,
                    total_cost=round(pos.total_cost, 2),
                    unrealized_pnl=None,
                    unrealized_pnl_percent=None,
                    price_available=False,
                    price_currency=quote.price_currency,
                    provider = quote.provider,
                    )
                )
            continue
        # If the currency is not the same as the one in my position, we pass
        if quote.currency and quote.currency != pos.currency:
            results.append(
                PnlRead(
                    symbol = pos.symbol,
                    currency = pos.currency,
                    quantity = round(pos.quantity,6),
                    average_cost=round(pos.average_cost, 2),
                    current_price=None,
                    market_value=None,
                    total_cost=round(pos.total_cost, 2),
                    unrealized_pnl=None,
                    unrealized_pnl_percent=None,
                    price_available=False,
                    price_currency=quote.price_currency,
                    provider = quote.provider,
                    )
                )
            continue

        market_value = pos.quantity * quote.price
        unrealized_pnl = market_value - pos.total_cost
        unrealized_pnl_percent = ((unrealized_pnl / pos.total_cost) * 100 if pos.total_cost > 0 else None)
        

        results.append(
            PnlRead(
                symbol=pos.symbol,
                currency=pos.currency,
                quantity=round(pos.quantity, 6),
                average_cost=round(pos.average_cost, 2),
                current_price=round(quote.price, 2),
                market_value=round(market_value, 2),
                total_cost=round(pos.total_cost, 2),
                unrealized_pnl=round(unrealized_pnl, 2),
                unrealized_pnl_percent=(
                    round(unrealized_pnl_percent, 2)
                    if unrealized_pnl_percent is not None
                    else None
                ),
                price_available=True,
                price_currency=quote.currency,
                provider=quote.provider,
            )
        )
    return results