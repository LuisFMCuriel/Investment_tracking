from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.ai.agent import portfolio_agent


APP_NAME = "portfolio_tracker"
USER_ID = "local_user"
SESSION_ID = "default_session"

session_service = InMemorySessionService()

runner = Runner(
    agent=portfolio_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def ask_portfolio_agent(message: str) -> str:
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text=message)],
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    return final_response