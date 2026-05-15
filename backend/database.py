import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default to SQLite for local dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./contracts.db")
print(f"Database Configured: {DATABASE_URL}")

# Ensure we are using SQLite
if not DATABASE_URL.startswith("sqlite"):
    raise ValueError("Using SQLite is now mandatory. Please ensure DATABASE_URL starts with 'sqlite'.")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
