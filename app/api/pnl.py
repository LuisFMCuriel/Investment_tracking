from fastapi import APIRouter, Depends
from app.schemas.pnl import PnLSummary
from app.services.pnl_service import get_pnl

#From our database
from sqlalchemy.orm import Session
from app.db.deps import get_db
router = APIRouter(tags=["pnl"])

@router.get("/pnl", response_model=PnLSummary)
def read_pnl(db: Session = Depends(get_db)) -> PnLSummary:
    """
    Get the current PnL summary for the portfolio.
    """
    return get_pnl(db)