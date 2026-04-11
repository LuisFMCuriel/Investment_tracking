from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.portfolio import PortfolioSummarySimple
from app.services.portfolio_service import PORTFOLIO


router = APIRouter(tags=["portfolio"])

@router.get("/portfolio", response_model=PortfolioSummarySimple)
def read_portfolio(db: Session = Depends(get_db)) -> PortfolioSummarySimple:
    return PORTFOLIO.get_portfolio_summary(db)
    #return get_portfolio_summary(db)