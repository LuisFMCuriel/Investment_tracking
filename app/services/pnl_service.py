from sqlalchemy.orm import Session

from app.schemas.pnl import PnlRead, PnLSummary
from app.services.market_data_service import get_current_price
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
        current_price = get_current_price(pos.symbol)
        market_value = pos.quantity * current_price
        total_cost = pos.total_cost
        unrealized_pnl = market_value - total_cost

        unrealized_pnl_percent = 0.0
        if total_cost > 0:
            unrealized_pnl_percent = (unrealized_pnl / total_cost) * 100

            results.append(
                PnlRead(
                    symbol = pos.symbol,
                    quantity = pos.quantity,
                    average_cost = round(pos.average_cost, 2),
                    current_price = round(current_price, 2),
                    market_value = round(market_value, 2),
                    total_cost = round(total_cost, 2),
                    unrealized_pnl = round(unrealized_pnl, 2),
                    unrealized_pnl_percent = round(unrealized_pnl_percent, 2),
                    )
                )
    return results