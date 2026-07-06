import sys
from pathlib import Path

from sqlmodel import Session, select

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import create_db_and_tables, engine
from app.models import User
from app.security import get_password_hash

# Define dummy users
DUMMY_USERS = [
    {
        "name": "Alice Vance",
        "email": "alice.vance@example.com",
        "password": "securepassword123",
        "is_employed": True,
    },
    {
        "name": "Bob Miller",
        "email": "bob.miller@example.com",
        "password": "employeebob456",
        "is_employed": False,
    },
    {
        "name": "Charlie Smith",
        "email": "charlie.smith@example.com",
        "password": "charliepass789",
        "is_employed": True,
    },
    {
        "name": "Diana Prince",
        "email": "diana.prince@example.com",
        "password": "wonderwoman2026",
        "is_employed": False,
    },
]


def seed_data():
    """Seed the database with dummy users if they don't already exist."""
    print("Initializing database tables...")
    create_db_and_tables()

    print("Seeding dummy users...")
    with Session(engine) as session:
        for user_data in DUMMY_USERS:
            # Check if user already exists
            statement = select(User).where(User.email == user_data["email"])
            existing_user = session.exec(statement).first()

            if existing_user:
                print(f"[Skip] User with email {user_data['email']} already exists.")
            else:
                hashed_pw = get_password_hash(user_data["password"])
                new_user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    password=hashed_pw,
                    is_employed=user_data["is_employed"],
                )
                session.add(new_user)
                print(f"[Added] Created user: {user_data['name']}")

        session.commit()
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    seed_data()


def insert_db(user_data: User):

    with Session(engine) as session:
        statement = select(User).where(User.email == user_data["email"])
        existing_user = session.exec(statement).first()

        if existing_user:
            print(f"[Skip] User with email {user_data['email']} already exists.")
        else:
            hashed_pw = get_password_hash(user_data["password"])
            new_user = User(
                name=user_data["name"],
                email=user_data["email"],
                password=hashed_pw,
                is_employed=user_data["is_employed"],
            )
        session.add(new_user)
        print(f"[Added] Created user: {user_data['name']}")

        session.commit()
    print("Database seeding completed successfully!")


print(
    insert_db(
        {
            "name": "alu",
            "email": "ali@gmail.com",
            "password": "ali123",
            "is_employed": False,
        }
    )
)
