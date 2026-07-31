from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

# One absolute DB path so POST/seed/inspect all hit the same file,
# regardless of the process working directory.
DB_DIR = Path(__file__).resolve().parent.parent / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "user.db"

engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}", echo=False)


def create_db_and_tables():
    """Create the database tables if they do not exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session
