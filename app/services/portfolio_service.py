from app.schemas.portfolio import PortfolioSummary

def get_portfolio_summary() -> PortfolioSummary:
    # Later this function can read from DB, combine positions, and fetch live prices.
    return PortfolioSummary(
        total_value=100000.0,
        cash=20000.0,
        invested_value=80000.0,
        unrealized_pln=5000.0,
        currency="EUR"
    )