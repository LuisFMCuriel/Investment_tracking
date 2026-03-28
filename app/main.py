from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings

from app.api.portfolio import router as portfolio_router
from app.api.health import router as health_router
from app.api.positions import router as positions_router
from app.api.pnl import router as pnl_router
from app.api.transactions import router as transactions_router

from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()
    yield
    # Shutdown logic (optional for now)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Portfolio Tracker API"}

app.include_router(health_router)
app.include_router(portfolio_router)
app.include_router(positions_router)
app.include_router(pnl_router)
app.include_router(transactions_router)