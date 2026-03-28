from fastapi import APIRouter
from app.schemas.pnl import PnLSummary
from app.services.pnl_service import get_pnl_summary

router = APIRouter(tags=["pnl"])

@router.get("/pnl", respose_model=PnLSummary)
def read_pnl() -> PnLSummary:
    """
    Get the current PnL summary for the portfolio.
    """
    return get_pnl_summary()