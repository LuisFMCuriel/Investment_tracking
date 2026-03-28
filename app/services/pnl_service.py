from app.schemas.pnl import PnLSummary

def get_pnl_summary() -> PnLSummary:
    # Placeholder implementation - replace with actual logic to calculate PnL summary
    return PnLSummary(
        unrealized_pnl=240.00,
        daily_pnl=35.50,
        total_return_pct=4.12,
        currency="EUR"
    )