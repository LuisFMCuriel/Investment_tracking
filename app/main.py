from fastapi import FastAPI
from app.core.config import settings

from app.api.portfolio import router as portfolio_router
from app.api.health import router as health_router
from app.api.positions import router as positions_router
from app.api.pnl import router as pnl_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Portfolio Tracker API"}

app.include_router(health_router)
app.include_router(portfolio_router)
app.include_router(positions_router)
app.include_router(pnl_router)