from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base

# SQLite URL - local file (do not create the file here)
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"

# For SQLite, check_same_thread must be False to allow usage with FastAPI's threaded workers.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

# Session factory for route handlers and other DB usage.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy Session and ensures it is closed.
    Usage in route:
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables() -> None:
    """
    Create database tables from SQLAlchemy models' Base metadata.
    Call this at application startup if you want to create tables programmatically.
    """
    Base.metadata.create_all(bind=engine)
