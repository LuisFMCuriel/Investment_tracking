# app/ai/agent.py

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from app.ai.tools import (
    portfolio_summary_tool,
    positions_tool,
    pnl_tool,
)


portfolio_agent = Agent(
    name="portfolio_readonly_agent",
    model=LiteLlm(model="ollama_chat/llama3.1"),
    description="Read-only portfolio assistant.",
    instruction="""
You are a read-only portfolio assistant.

You can answer questions about:
- portfolio summary
- positions
- unrealized PnL
- basic portfolio interpretation

Rules:
- Never create, update, or delete data.
- Never execute trades.
- Never give financial advice as a recommendation to buy or sell.
- Use the available tools when answering portfolio-specific questions.
- If data is missing, say what is missing.
""",
    tools=[
        portfolio_summary_tool,
        positions_tool,
        pnl_tool,
    ],
)