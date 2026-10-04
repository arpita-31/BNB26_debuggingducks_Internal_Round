"""
Database Engine and Session Factory for ReLearn
Configures SQLite with thread safety and provides session dependency.
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base

DB_PATH = Path(__file__).resolve().parent.parent.parent / "relearn.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates all database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI dependency for database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
