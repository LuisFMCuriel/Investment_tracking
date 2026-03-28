from fastapi import APIRouter
from app.schemas.position import Position
from app.services.position_service import get_positions

router = APIRouter(tags=["positions"])

@router.get("/positions", response_model=list[Position])
def read_positions() -> list[Position]:
    """
    Get a list of all positions in the portfolio.
    """
    return get_positions()