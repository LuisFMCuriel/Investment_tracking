from pydantic import BaseModel
from fastapi import APIRouter

from app.ai.service import ask_portfolio_agent


router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest) -> ChatResponse:
    response = await ask_portfolio_agent(request.message)
    return ChatResponse(response=response)