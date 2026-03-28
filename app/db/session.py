from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./portfolio.db"
# The engine is the connection to the database
# check_same_thread is set to False because SQLite 
# does not allow multiple 
# threads to access the same database connection
engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False})
# Factory for creating new database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)