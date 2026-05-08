# app/ai/tools.py

from app.services.portfolio_service import get_portfolio_summary
from app.services.position_service import get_positions
from app.services.pnl_service import get_pnl


def portfolio_summary_tool() -> dict:
    """Return the current portfolio summary."""
    return get_portfolio_summary().model_dump()


def positions_tool() -> list[dict]:
    """Return all current portfolio positions."""
    return [position.model_dump() for position in get_positions()]


def pnl_tool() -> list[dict]:
    """Return current profit and loss per position."""
    return [item.model_dump() for item in get_pnl()]