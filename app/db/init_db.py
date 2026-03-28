from app.db.base import Base
from app.db.session import engine
# This is my model from sqlalchemy
from app.models.transactions import Transaction

def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)