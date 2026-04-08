from fastapi import APIRouter, Depends
from app.services.position_service import get_positions
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.position import PositionRead

router = APIRouter(tags=["positions"])

@router.get("/positions", response_model=list[PositionRead])
def read_positions(db:Session = Depends(get_db)) -> list[PositionRead]:
    """
    Get a list of all positions in the portfolio.
    """
    return get_positions(db)