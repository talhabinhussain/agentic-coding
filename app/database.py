from pathlib import Path

from sqlmodel import SQLModel, Session, create_engine

DB_PATH = Path(__file__).resolve().parent / "database.db"
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Create the database tables if they do not exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session
