from fastapi import APIRouter
from app.schemas.portfolio import PortfolioSummary
from app.services.portfolio_service import get_portfolio_summary

router = APIRouter(tags=["portfolio"])

@router.get("/portfolio", response_model=PortfolioSummary)
def read_portfolio() -> PortfolioSummary:
    """
    Get a summary of the user's investment portfolio.
    """
    return get_portfolio_summary()