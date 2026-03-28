from collections.abc import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
# Dependency to get a database session for each request
# db is a generator that yields a database session and ensures it is closed after the request is done
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()